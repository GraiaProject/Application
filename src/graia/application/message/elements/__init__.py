import abc
from typing import Any
from pydantic import BaseModel


class Element(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class InternalElement(Element, abc.ABC):
    def toExternal(self) -> "ExternalElement":
        """可以为异步方法"""
        pass

    @abc.abstractclassmethod
    def fromExternal(cls, external_element) -> "InternalElement":
        """可以为异步方法"""
        pass

    def asDisplay(self) -> str:
        return ""

    def asSerializationString(self) -> str:
        return ""


class ExternalElement(Element):
    pass


class ShadowElement(Element):
    pass


def isShadowElement(any_instance: Any) -> bool:
    """检查实例是否为 Shadow Element

    Args:
        any_instance (Any): 欲检查的实例

    Returns:
        bool: 是否为 Shadow Element
    """
    return isinstance(any_instance, ShadowElement)
