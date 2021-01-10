import shlex

from typing import Dict, List, Tuple
from graia.application.message.chain import MessageChain, MessageIndex
from graia.application.message.elements import Element
from graia.application.message.elements.internal import Plain

from graia.application.message.parser.pattern import (
    BoxParameter,
    ParamPattern,
    SwitchParameter,
)


class Literature:
    "旅途的浪漫"

    prefixs: Tuple[str]  # 匹配前缀
    delimiter: str = " "  # 分割符
    param_settings: Dict[str, ParamPattern]
    param_settings_index: Dict[str, Tuple[str, ParamPattern]]  # 匹配文本, 参数名, 设置

    def __init__(
        self, *prefixs, parameters: Dict[str, ParamPattern], delimiter: str = None
    ) -> None:
        self.prefixs = prefixs
        self.param_settings = parameters

        indexes = {}
        for param_name, setting in parameters.items():
            for keyword in setting.keywords:
                if keyword in indexes:
                    raise ValueError(f"{keyword} 重复了")  # TODO: English
                indexes[keyword] = (param_name, setting)
        self.param_settings_index = indexes
        if delimiter:
            self.delimiter = delimiter

    def detect_index(self, target_chain: MessageChain):
        target_chain = target_chain.asMerged()
        current_index: MessageIndex = (0, None)
        start_index: MessageIndex = (0, None)
        detect_result: Dict[str, List[Tuple[MessageIndex, MessageIndex]]] = {
            "_": []  # 相当于 *args.
        }

        chain_frames: List[MessageChain] = target_chain.split(self.delimiter)

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
        for index, current_frame in enumerate(chain_frames):
            if not current_frame.__root__:
                collections.append(current_frame)
                continue
            if (
                current_frame.asDisplay() not in self.param_settings_index
            ) and not detecting_param:
                collections.append(current_frame)
                continue

            if detecting_param:
                detect_result[detecting_param] = current_frame
                detecting_param = None
                continue

            param_name, setting = self.param_settings_index[current_frame.asDisplay()]
            if param_name in detect_result:
                continue  # 用户重复输入了参数

            if isinstance(setting, SwitchParameter):  # 这里是已经被 catch 到了.
                if setting.auto_reverse:
                    detect_result[param_name] = not setting.default
                else:
                    detect_result[param_name] = True
            elif isinstance(setting, BoxParameter):
                afters = MessageChain.join(*chain_frames[index + 1 :])
                if afters.startswith('"'):
                    param_content = []
                    for elem in afters.subchain(
                        slice((0, 1), None, None), ignore_text_index=True
                    ):
                        if isinstance(elem, Plain):
                            continue_flag = False
                            for text_index, text_i in enumerate(elem.text):
                                if continue_flag:
                                    continue_flag = False
                                    continue
                                if text_i == "\\":
                                    continue_flag = True
                                if text_i == '"':
                                    param_content.append(
                                        Plain(elem.text[: text_index + 1])
                                    )
                                    break
                            else:
                                # 没找到
                                param_content.append(elem)
                                break
                        else:
                            param_content.append(elem)
                            break
                    else:
                        raise ValueError("no closing quotes")

                    detect_result[param_name] = MessageChain.create(param_content)
                else:
                    detecting_param = param_name
        else:
            if detecting_param:
                raise ValueError("require for " + detecting_param)
        return detect_result


if __name__ == "__main__":
    from graia.application.message.elements.internal import AtAll

    mc = MessageChain.create([Plain("test n -gta")])
    l = Literature(
        "test",
        "n",
        parameters={
            "n1": SwitchParameter(["--bool-test", "-bt"]),
            "n2": BoxParameter(["-gt"]),
        },
    )
    print("returned:", l.detect_index(mc))
