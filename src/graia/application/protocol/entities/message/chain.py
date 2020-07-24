from __future__ import annotations
from typing import (Any, Dict, Generic, List, Sequence, Tuple, Type, TypeVar,
                    Union)

from devtools import debug

from graia.application.protocol.exceptions import EntangledSuperposition
from graia.broadcast.utilles import printer, run_always_await
from pydantic import BaseModel, validator
from graia.application.context import event_loop

from .elements import external as External
from . import ExternalElement, InternalElement

T = Union[InternalElement, ExternalElement]

class MessageChain(BaseModel):
    __root__: Union[List[T], Tuple[T]]
    
    @classmethod
    def parse_obj(cls: Type['MessageChain'], obj: List[T]) -> 'MessageChain':
        "将其构建为内部态."
        handled_elements = []
        for i in obj:
            if isinstance(i, InternalElement):
                handled_elements.append(i)
            elif isinstance(i, ExternalElement):
                for ii in InternalElement.__subclasses__():
                    if ii.__name__ == i.__class__.__name__:
                        handled_elements.append(ii.fromExternal(i))
            elif isinstance(i, dict) and "type" in i:
                for ii in ExternalElement.__subclasses__():
                    if ii.__name__ == i['type']:
                        for iii in InternalElement.__subclasses__():
                            if iii.__name__ == i['type']:
                                handled_elements.append(iii.fromExternal(ii.parse_obj(i)))
        return cls(__root__=handled_elements)

    @property
    def isImmutable(self):
        return isinstance(self.__root__, tuple)

    def asMutable(self) -> "MessageChain":
        return MessageChain(__root__=list(self.__root__))

    def asImmutable(self) -> "MessageChain":
        return MessageChain(__root__=tuple(self.__root__))

    @property
    def isSendable(self) -> bool:
        return all(isinstance(i, InternalElement) and hasattr(i, "toExternal") for i in self.__root__)

    async def build(self, **extra: Dict[InternalElement, Tuple[list, dict]]) -> "MessageChain":
        debug(self.__root__)
        return MessageChain(tuple([await run_always_await(i.toExternal(
            *(extra[i.__class__][0] if i.__class__ in extra else []),
            **(extra[i.__class__][1] if i.__class__ in extra else {})
        )) if isinstance(i, InternalElement) else i for i in self.__root__]))

    def has(self, element_class: T) -> bool:
        return element_class in [type(i) for i in self.__root__]

    def get(self, element_class: T) -> List[T]:
        return [i for i in self.__root__ if isinstance(i, element_class)]

    def asDisplay(self) -> str:
        return "".join(i.asDisplay() for i in self.__root__)

    @classmethod
    def join(cls, *chains: List["MessageChain"]) -> "MessageChain":
        return cls(sum(chains, []))

    __contains__ = has
    __getitem__ = get

