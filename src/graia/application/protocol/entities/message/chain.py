from __future__ import annotations
from typing import (Any, Callable, Dict, Generic, List, Optional, Sequence, Tuple, Type, TypeVar,
                    Union, cast)
import warnings

from devtools import debug

from graia.application.protocol.exceptions import EntangledSuperposition
from graia.broadcast.utilles import printer, run_always_await
from pydantic import BaseModel, validator
from graia.application.context import event_loop

from .elements import external as External
from . import ExternalElement, InternalElement

T = Union[InternalElement, ExternalElement]

def raiser(error):
    raise error

class MessageChain(BaseModel):
    __root__: Union[List[T], Tuple[T]]

    @classmethod
    def create(cls, elements: Sequence[T]):
        return cls(__root__=elements)

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
        return cls(__root__=tuple(handled_elements)) # 默认是不可变型

    @property
    def isImmutable(self):
        return isinstance(self.__root__, tuple)

    def asMutable(self) -> "MessageChain":
        return MessageChain(__root__=list(self.__root__))

    def asImmutable(self) -> "MessageChain":
        return MessageChain(__root__=tuple(self.__root__))

    @property
    def isSendable(self) -> bool:
        return all(all([
            isinstance(i, (InternalElement, ExternalElement)),
            hasattr(i, "toExternal"),
            getattr(i.__class__, "toExternal") != InternalElement.toExternal
        ]) for i in self.__root__)

    def asSendable(self) -> "MessageChain":
        return MessageChain(__root__=tuple([i for i in self.__root__ if all([
            isinstance(i, InternalElement),
            hasattr(i, "toExternal"),
            getattr(i.__class__, "toExternal") != InternalElement.toExternal
        ])]))

    async def build(self, **extra: Dict[InternalElement, Tuple[list, dict]]) -> "MessageChain":
        result = []
        for i in self.__root__:
            if isinstance(i, InternalElement):
                if getattr(i.__class__, "toExternal") == InternalElement.toExternal:
                    raise EntangledSuperposition("You define an object that cannot be sent: {0}".format(i.__class__.__name__))
                result.append(await run_always_await(i.toExternal(
                    *(extra[i.__class__][0] if i.__class__ in extra else []),
                    **(extra[i.__class__][1] if i.__class__ in extra else {})
                )))
            else:
                result.append(i)
        return MessageChain(__root__=tuple(result))

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

