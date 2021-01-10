from typing import Any, List
from dataclasses import dataclass


@dataclass(init=True, eq=True, repr=True)
class ParamPattern:
    keywords: List[str]
    default: Any = None


@dataclass(init=True, eq=True, repr=True)
class SwitchParameter(ParamPattern):
    default: bool = False
    auto_reverse: bool = False


@dataclass(init=True, eq=True, repr=True)
class BoxParameter(ParamPattern):
    "可以被指定传入消息的参数, 但只有一个."
