import abc
from pydantic import BaseModel

class Element(BaseModel):
    pass

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