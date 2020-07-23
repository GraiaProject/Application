from typing import Optional
from pydantic.class_validators import validator
from . import ExternalElement
from ..chain import MessageChain

class Image(ExternalElement):
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

class Quote(ExternalElement):
    id: int
    groupId: int
    senderId: int
    targetId: int
    origin: MessageChain

    @validator("origin")
    def _(cls, v):
        return MessageChain.parse_obj(v)

class FlashImage(Image):
    pass