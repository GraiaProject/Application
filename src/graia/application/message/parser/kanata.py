from functools import lru_cache
import functools
from types import TracebackType
from typing import Dict, List, Optional, Tuple, TypeVar, Union
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.signatures import Force
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.broadcast.builtin.factory import (
    AsyncDispatcherContextManager,
    ResponseCodeEnum,
    StatusCodeEnum,
)

from graia.application.exceptions import ConflictItem

from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import (
    At,
    FlashImage,
    Plain,
    Source,
    Quote,
    Voice,
    Xml,
    Json,
    App,
    Poke,
)
from .signature import FullMatch, NormalMatch, PatternReceiver
from .pack import Arguments, merge_signature_chain
from graia.application.utilles import InsertGenerator
from .signature import RequireParam, OptionalParam
import re
import random
import copy

BLOCKING_ELEMENTS = (Xml, Json, App, Poke, Voice, FlashImage)

T = Union[NormalMatch, PatternReceiver]
MessageIndex = Tuple[int, Optional[int]]
_T = TypeVar("_T")


def origin_or_zero(origin: Optional[_T]) -> Union[_T, int]:
    if origin is None:
        return 0
    return origin


class Kanata(AsyncDispatcherContextManager):
    "彼方."
    signature_list: List[Union[NormalMatch, PatternReceiver]]
    stop_exec_if_fail: bool = True

    parsed_items: Dict[str, MessageChain]

    allow_quote: bool
    skip_one_at_in_quote: bool

    args = ()
    kwargs = {}

    def __init__(
        self,
        signature_list: List[Union[NormalMatch, PatternReceiver]],
        stop_exec_if_fail: bool = True,
        allow_quote: bool = True,
        skip_one_at_in_quote: bool = False,
    ) -> None:
        """该魔法方法用于实例化该参数解析器.

        Args:
            signature_list (List[Union[NormalMatch, PatternReceiver]]): 匹配标识链
            stop_exec_if_fail (bool, optional): 是否在无可用匹配时停止监听器执行. Defaults to True.
            allow_quote (bool, optional): 是否允许 Kanata 处理回复消息中的用户输入部分. Defaults to True.
            skip_one_at_in_quote (bool, optional): 是否允许 Kanata 在处理回复消息中的用户输入部分时自动删除可能\
                由 QQ 客户端添加的 At 和一个包含在单独 Plain 元素中的空格. Defaults to False.
        """
        self.signature_list = signature_list
        self.stop_exec_if_fail = stop_exec_if_fail
        self.parsed_items = None
        self.allow_quote = allow_quote
        self.skip_one_at_in_quote = skip_one_at_in_quote

    @staticmethod
    def detect_index(
        signature_chain: Tuple[Union[NormalMatch, PatternReceiver]],
        message_chain: MessageChain,
    ) -> Optional[Dict[str, Tuple[MessageIndex, MessageIndex]]]:
        merged_chain = merge_signature_chain(signature_chain)
        message_chain = message_chain.asMerged()
        element_num = len(message_chain.__root__)
        end_index: MessageIndex = (
            element_num - 1,
            len(message_chain.__root__[-1].text)
            if element_num != 0 and message_chain.__root__[-1].__class__ is Plain
            else None,
        )

        reached_message_index: MessageIndex = (0, None)
        # [0] => real_index
        # [1] => text_index(optional)

        start_index: MessageIndex = (0, None)

        match_result: Dict[
            Arguments,
            Tuple[MessageIndex, MessageIndex],  # start(include)  # stop(exclude)
        ] = {}

        signature_iterable = InsertGenerator(enumerate(merged_chain))
        latest_index = None
        matching_recevier: Optional[Arguments] = None

        for signature_index, signature in signature_iterable:
            if isinstance(signature, (Arguments, PatternReceiver)):
                if matching_recevier:  # 已经选中了一个...
                    if isinstance(signature, Arguments):
                        if latest_index == signature_index:
                            matching_recevier.content.extend(signature.content)
                            continue
                        else:
                            raise TypeError("a unexpected case: match conflict")
                    if isinstance(signature, PatternReceiver):
                        matching_recevier.content.append(signature)
                        continue
                else:
                    if isinstance(signature, PatternReceiver):
                        signature = Arguments([signature])
                matching_recevier = signature
                start_index = reached_message_index
            elif isinstance(signature, NormalMatch):
                if not matching_recevier:
                    # 如果不要求匹配参数, 从当前位置(reached_message_index)开始匹配FullMatch.
                    current_chain = message_chain.subchain(
                        slice(reached_message_index, None, None)
                    )
                    if not current_chain.__root__:  # index 越界
                        return
                    if not isinstance(current_chain.__root__[0], Plain):
                        # 切片后第一个 **不是** Plain.
                        return
                    re_match_result = re.match(
                        signature.operator(), current_chain.__root__[0].text
                    )
                    if not re_match_result:
                        # 不匹配的
                        return
                    # 推进当前进度.
                    plain_text_length = len(current_chain.__root__[0].text)
                    pattern_length = re_match_result.end() - re_match_result.start()
                    if (pattern_length + 1) > plain_text_length:  # 推进后可能造成错误
                        # 不推进 text_index 进度, 转而推进 element_index 进度
                        reached_message_index = (reached_message_index[0] + 1, None)
                    else:
                        # 推进 element_index 进度至已匹配到的地方后.
                        reached_message_index = (
                            reached_message_index[0],
                            origin_or_zero(reached_message_index[1])
                            + re_match_result.start()
                            + pattern_length,
                        )
                else:
                    # 需要匹配参数(是否贪婪模式查找, 即是否从后向前)
                    greed = matching_recevier.isGreed
                    for element_index, element in enumerate(
                        message_chain.subchain(
                            slice(reached_message_index, None, None)
                        ).__root__
                    ):
                        if isinstance(element, Plain):
                            current_text: str = element.text
                            # 完成贪婪判断
                            text_find_result_list = list(
                                re.finditer(signature.operator(), current_text)
                            )
                            if not text_find_result_list:
                                continue
                            text_find_result = text_find_result_list[-int(greed)]
                            if not text_find_result:
                                continue
                            text_find_index = text_find_result.start()

                            # 找到了! 这里不仅要推进进度, 还要把当前匹配的参数记录结束位置并清理.
                            stop_index = (
                                reached_message_index[0]
                                + element_index
                                + int(element_index == 0),
                                origin_or_zero(reached_message_index[1])
                                + text_find_index,
                            )
                            match_result[matching_recevier] = (
                                copy.copy(start_index),
                                stop_index,
                            )

                            start_index = (0, None)
                            matching_recevier = None

                            pattern_length = (
                                text_find_result.end() - text_find_result.start()
                            )
                            if (
                                current_text
                                == text_find_result.string[
                                    slice(*text_find_result.span())
                                ]
                            ):
                                # 此处是如果推进 text_index 就会被爆破....
                                # 推进 element_index 而不是 text_index
                                reached_message_index = (
                                    reached_message_index[0]
                                    + element_index
                                    + int(element_index != 0),
                                    None,
                                )
                            else:
                                reached_message_index = (
                                    reached_message_index[0] + element_index,
                                    origin_or_zero(reached_message_index[1])
                                    + text_find_index
                                    + pattern_length,
                                )
                            break
                    else:
                        # 找遍了都没匹配到.
                        return
            latest_index = signature_index
        else:
            if matching_recevier:  # 到达了终点, 却仍然还要做点事的.
                # 计算终点坐标.
                text_index = None

                latest_element = message_chain.__root__[-1]
                if isinstance(latest_element, Plain):
                    text_index = len(latest_element.text)

                stop_index = (len(message_chain.__root__), text_index)
                match_result[matching_recevier] = (start_index, stop_index)
            else:  # 如果不需要继续捕获消息作为参数, 但 Signature 已经无法指示 Message 的样式时, 判定本次匹配非法.
                if reached_message_index < end_index:
                    return

        return match_result

    @staticmethod
    def detect_and_mapping(
        signature_chain: Tuple[Union[NormalMatch, PatternReceiver]],
        message_chain: MessageChain,
    ) -> Optional[Dict[Arguments, MessageChain]]:
        match_result = Kanata.detect_index(signature_chain, message_chain)
        if match_result is not None:
            return {
                k: message_chain[
                    v[0] : (
                        v[1][0],
                        (
                            v[1][1]
                            - (
                                origin_or_zero(v[0][1])
                                if (v[1][0] <= v[0][0] <= v[1][0])
                                else 0
                            )
                        )
                        if v[1][1] is not None
                        else None,
                    )
                ]
                for k, v in match_result.items()
            }

    @staticmethod
    def allocation(
        mapping: Dict[Arguments, MessageChain]
    ) -> Optional[Dict[str, MessageChain]]:
        if mapping is None:
            return None
        result = {}
        for arguemnt_set, message_chain in mapping.items():
            length = len(arguemnt_set.content)
            for index, receiver in enumerate(arguemnt_set.content):
                if receiver.name in result:
                    raise ConflictItem("{0} is defined repeatedly".format(receiver))
                if isinstance(receiver, RequireParam):
                    if not message_chain.__root__:
                        return
                    result[receiver.name] = message_chain
                elif isinstance(receiver, OptionalParam):
                    if not message_chain.__root__:
                        result[receiver.name] = None
                    else:
                        result[receiver.name] = message_chain
                break  # 还没来得及做长度匹配...
        return result

    @lru_cache(None)
    async def catch_argument_names(self) -> List[str]:
        return [i.name for i in self.signature_list if isinstance(i, PatternReceiver)]

    async def generator_factory(self):
        interface: DispatcherInterface = (yield)
        current_status: StatusCodeEnum = StatusCodeEnum.DISPATCHING  # init stat

        message_chain: MessageChain = (
            await interface.lookup_param("__kanata_messagechain__", MessageChain, None)
        ).exclude(Source)
        if set([i.__class__ for i in message_chain.__root__]).intersection(
            BLOCKING_ELEMENTS
        ):
            raise ExecutionStop()
        if self.allow_quote and message_chain.has(Quote):
            # 0: Quote
            message_chain = message_chain[(1, None):]
            if self.skip_one_at_in_quote and message_chain.__root__:
                if message_chain.__root__[0].__class__ is At:
                    message_chain = message_chain[(1, 1):]

        mapping_result = self.detect_and_mapping(self.signature_list, message_chain)
        if mapping_result is not None:
            parsed_items = self.allocation(mapping_result)
        else:
            if self.stop_exec_if_fail:
                raise ExecutionStop()
        yield
        while current_status is StatusCodeEnum.DISPATCHING:
            result = None

            if interface.name != "__kanata_messagechain__":
                random_id = random.random()
                if parsed_items is not None:
                    item = parsed_items.get(interface.name, random_id)
                    result = Force(item) if item is not random_id else None
                else:
                    if self.stop_exec_if_fail:
                        raise ExecutionStop()

            current_status, external = yield (ResponseCodeEnum.VALUE, result)
