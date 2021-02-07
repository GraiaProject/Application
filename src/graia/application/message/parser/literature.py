from typing import Dict, List, Tuple
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.signatures import Force
from graia.broadcast.exceptions import ExecutionStop

from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.broadcast.utilles import printer
from graia.application.message.chain import MessageChain, MessageIndex
from graia.application.message.elements import Element
from graia.application.message.elements.internal import (
    App,
    Json,
    Plain,
    Quote,
    Source,
    Xml,
    Voice,
    Poke,
    FlashImage,
)

from graia.application.message.parser.pattern import (
    BoxParameter,
    ParamPattern,
    SwitchParameter,
)
from graia.application.utilles import MultiUsageGenerator

BLOCKING_ELEMENTS = (Xml, Json, App, Poke, Voice, FlashImage)


async def async_tb_printer(coro):
    try:
        return await coro
    except:
        import traceback

        traceback.print_exc()


class Literature(BaseDispatcher):
    "旅途的浪漫"

    always = False
    prefixs: Tuple[str]  # 匹配前缀
    delimiter: str = " "  # 分割符
    param_settings: Dict[str, ParamPattern]
    param_settings_index: Dict[str, Tuple[str, ParamPattern]]  # 匹配文本, 参数名, 设置

    def __init__(
        self,
        *prefixs,
        parameters: Dict[str, ParamPattern],
        delimiter: str = None,
        use_help_param: bool = True,
    ) -> None:
        self.prefixs = prefixs

        if use_help_param:
            parameters["__help_param__"] = SwitchParameter(["-h", "--help"])
        self.param_settings = parameters

        indexes = {}
        for param_name, setting in parameters.items():
            for keyword in setting.keywords:
                if keyword in indexes:
                    raise ValueError(f"duplicate keywords {keyword}")  # TODO: English
                indexes[keyword] = (param_name, setting)
        self.param_settings_index = indexes
        if delimiter:
            self.delimiter = delimiter

    def detect_index(self, target_chain: MessageChain):
        target_chain = target_chain.asMerged()
        detect_result: Dict[str, List[Tuple[MessageIndex, MessageIndex]]] = {
            "_": []  # 相当于 *args.
        }

        chain_frames: List[MessageChain] = target_chain.split(
            self.delimiter, raw_string=True
        )

        # 前缀匹配
        if len(self.prefixs) > len(chain_frames):
            return
        for index in range(len(self.prefixs)):
            current_prefix = self.prefixs[index]
            current_frame = chain_frames[index]
            if (
                not current_frame.__root__
                or type(current_frame.__root__[0]) is not Plain
            ):
                return
            if current_frame.__root__[0].text != current_prefix:
                return

        chain_frames = chain_frames[len(self.prefixs) :]  # 清除无关数据, 开始执行.

        collections: List[Element] = detect_result["_"]

        detecting_param = None
        local_iter = MultiUsageGenerator(enumerate(chain_frames))
        # print(list(local_iter))
        for iter_item in local_iter:
            print(92, iter_item)
            index, current_frame = iter_item
            current_frame: MessageChain
            if not current_frame.__root__:
                collections.append(current_frame)
                continue

            if detecting_param and isinstance(
                self.param_settings[detecting_param], BoxParameter
            ):
                detect_result[detecting_param] = current_frame
                detecting_param = None
                continue

            splited = current_frame.split("=", raw_string=True)
            origin_data = self.param_settings_index.get(splited[0].asDisplay())
            if not origin_data:
                if not detecting_param:
                    if current_frame.startswith('"'):  # TODO: 我现在还需要一个更加合理的引号出现判断.
                        # debug("ocur", index, chain_frames, current_frame)
                        afters_root = MessageChain.create(
                            sum(
                                [
                                    [*i.__root__, Plain(self.delimiter)]
                                    for i in chain_frames[max(0, index - 1) :]
                                ],
                                [],
                            )[:-1]
                        ).asMerged()
                        print("aftersRoot", index, afters_root)

                        break_flag_root = False
                        param_content_root = []
                        for elem in afters_root.subchain(
                            slice((0, 1), None, None), ignore_text_index=True
                        ):
                            print(elem)
                            if break_flag_root:
                                break_flag_root = False
                                break
                            if isinstance(elem, Plain):
                                continue_flag = False
                                for text_index, text_i in enumerate(elem.text):
                                    if continue_flag:
                                        continue_flag = False
                                        continue

                                    if text_i == "\\":
                                        continue_flag = True
                                    if text_i == '"':
                                        param_content_root.append(
                                            Plain(elem.text[:text_index])
                                        )
                                        break_flag_root = True
                                        break
                                else:
                                    # 没找到
                                    param_content_root.append(elem)
                                    break
                            else:
                                param_content_root.append(elem)
                                break
                        else:
                            if not break_flag_root:
                                raise ValueError("no closing quotes")
                        param_content_chain_root = MessageChain.create(
                            param_content_root
                        )
                        local_iter.continue_count += len(
                            param_content_chain_root.split(
                                self.delimiter, raw_string=True
                            )
                        )
                        collections.append(param_content_chain_root)
                    else:
                        collections.append(current_frame)
                continue
            param_name, setting = origin_data
            detecting_param = param_name
            if param_name in detect_result:
                continue  # 用户重复输入了参数

            if isinstance(setting, SwitchParameter):  # 这里是已经被 catch 到了.
                if setting.auto_reverse:
                    detect_result[param_name] = not setting.default
                else:
                    detect_result[param_name] = True
            elif isinstance(setting, BoxParameter):
                afters = MessageChain.create(
                    sum(
                        (
                            [i.__root__ for i in splited[1:]]
                            + [[Plain(self.delimiter)]]
                            if len(splited) > 1
                            else []
                        )
                        + [
                            [*i.__root__, Plain(self.delimiter)]
                            for i in chain_frames[index + 1 :]
                        ],
                        [],
                    )[:-1]
                ).asMerged()
                break_flag = False
                if afters.startswith('"'):
                    param_content = []
                    for elem in afters.subchain(
                        slice((0, 1), None, None), ignore_text_index=True
                    ):
                        if break_flag:
                            break_flag = False
                            break
                        if isinstance(elem, Plain):
                            continue_flag = False
                            for text_index, text_i in enumerate(elem.text):
                                if continue_flag:
                                    continue_flag = False
                                    continue

                                if text_i == "\\":
                                    continue_flag = True
                                if text_i == '"':
                                    param_content.append(Plain(elem.text[:text_index]))
                                    break_flag = True
                                    break
                            else:
                                # 没找到
                                param_content.append(elem)
                        else:
                            param_content.append(elem)
                    else:
                        if not break_flag:
                            raise ValueError("no closing quotes")
                    param_content_chain = MessageChain.create(param_content)
                    print(
                        param_content,
                        chain_frames[
                            len(
                                param_content_chain.split(
                                    self.delimiter, raw_string=True
                                )
                            )
                            + 1 :
                        ],
                    )
                    local_iter.continue_count += (
                        len(param_content_chain.split(self.delimiter, raw_string=True))
                        - 1
                    )
                    detect_result[param_name] = [MessageChain.create(param_content)]
                else:
                    detecting_param = param_name

                if len(splited) > 1 and not break_flag:
                    local_iter.insert_items.extend(
                        [
                            (index + l_index, value)
                            for l_index, value in enumerate(splited[1:], 1)
                        ]
                    )
                detecting_param = None
        else:
            if detecting_param and detecting_param not in detect_result:
                if self.param_settings[detecting_param].default is None:
                    raise ValueError("require for " + detecting_param)

        # 后处理
        for k, v in self.param_settings.items():
            if isinstance(v, SwitchParameter) and k not in detect_result:
                detect_result[k] = v.default
            elif isinstance(v, BoxParameter) and k not in detect_result:
                detect_result[k] = Force(None)
        return detect_result

    async def beforeDispatch(self, interface: DispatcherInterface):
        try:
            message_chain: MessageChain = (
                await interface.lookup_param(
                    "__literature_messagechain__", MessageChain, None
                )
            ).exclude(Source)
            if set([i.__class__ for i in message_chain.__root__]).intersection(
                BLOCKING_ELEMENTS
            ):
                raise ExecutionStop()
            interface.execution_contexts[-1].literature_detect_result = printer(
                self.detect_index(message_chain)
            )
        except:
            import traceback

            traceback.print_exc()

    async def catch(self, interface: DispatcherInterface):
        if interface.name == "__literature_messagechain__":
            return

        result = interface.execution_contexts[-1].literature_detect_result
        if result:
            param_value = result.get(interface.name)
            return param_value


if __name__ == "__main__":
    from graia.application.message.elements.internal import AtAll, At

    mc = MessageChain.create(
        [
            Plain('test n -gt "1 2 tsthd thsd ydj re7u  '),
            At(351453455),
            Plain(' " "arg arega er ae aghr ae rtyh'),
            At(656735757),
            Plain(' "'),
        ]
    )
    l = Literature(
        "test",
        "n",
        parameters={
            "n1": SwitchParameter(["--bool-test", "-bt"]),
            "n2": BoxParameter(["-gt"]),
        },
    )
    from devtools import debug

    debug(l.detect_index(mc))
    print(mc.asDisplay())
