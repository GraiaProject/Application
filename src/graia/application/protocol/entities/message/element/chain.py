from typing import Any, Dict, Generic, List, Sequence, Tuple, Type, TypeVar, Union
from pydantic import BaseModel, validator

from graia.application.protocol.entities.message import element
from graia.application.protocol.exceptions import EntangledSuperposition
from .elements import InternalElement, ExternalElement
from .elements import external as External
from graia.broadcast.utilles import run_always_await

T = TypeVar("T", ExternalElement, InternalElement)
U = TypeVar("U", Tuple, List)

class MessageChain(BaseModel, Generic[T, U]):
    __root__: Sequence[U[T]]
    
    def __init__(self, elements: Sequence[U[T]]) -> None:
        super(MessageChain, self).__init__(
            __root__=elements
        )

    @classmethod
    @validator("__root__")
    def _(cls, v):
        chain_types = [isinstance(i, InternalElement) for i in v\
            if isinstance(i, (ExternalElement, InternalElement))]
        if len(list(set(chain_types))) != 1:
            raise EntangledSuperposition("you cannot put both internal element and external element into a chain!")
        return v

    @classmethod
    async def parse_obj(cls: Type['MessageChain'], obj: List[T]) -> 'MessageChain':
        "将其构建为内部态."
        handled_elements = []
        for i in obj:
            if isinstance(i, External.Quote):
                handled_elements.append(External.Quote.parse_obj(i))
            elif isinstance(i, InternalElement):
                handled_elements.append(i)
            elif isinstance(i, ExternalElement):
                for ii in InternalElement.__subclasses__():
                    if ii.__name__ == i.__class__.__name__:
                        handled_elements.append(await run_always_await(ii.fromExternal(i)))
            elif isinstance(i, dict) and "type" in i:
                for ii in ExternalElement.__subclasses__():
                    if ii.__name__ == i['type']:
                        for iii in InternalElement.__subclasses__():
                            if iii.__name__ == i['type']:
                                handled_elements.append(await run_always_await(
                                    iii.fromExternal(i.parse_obj(i)))
                                )
        return super().parse_obj(handled_elements)

    @property
    def isImmutable(self):
        return isinstance(self.__root__, tuple)

    def asMutable(self) -> "MessageChain[T, List]":
        return MessageChain(__root__=list(self.__root__))

    def asImmutable(self) -> "MessageChain[T, Tuple]":
        return MessageChain(__root__=tuple(self.__root__))

    @property
    def isSendable(self) -> bool:
        return all(isinstance(i, InternalElement) and hasattr(i, "toExternal") for i in self.__root__)

    async def build(self, **extra: Dict[InternalElement, Tuple[list, dict]]) -> "MessageChain[ExternalElement, Tuple]":
        return MessageChain(
            __root__=tuple(await run_always_await(i.toExternal(
                *(extra[i.__class__][0] if i.__class__ in extra else []), 
                **(extra[i.__class__][1] if i.__class__ in extra else {})
            )) if isinstance(i, InternalElement) else i for i in self.__root__)
        )

    def has(self, element_class: T) -> bool:
        return element_class in [type(i) for i in self.__root__]

    def get(self, element_class: T) -> List[T]:
        return [i for i in self.__root__ if isinstance(i, element_class)]

    def asDisplay(self) -> str:
        return "".join(i.asDisplay() for i in self.__root__)

    @classmethod
    def join(cls, *chains: List["MessageChain[T, U]"]) -> "MessageChain[T, U]":
        return cls(sum(chains, []))

    __contains__ = has
    __getitem__ = get