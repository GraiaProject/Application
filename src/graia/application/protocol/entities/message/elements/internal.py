import asyncio
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Union

from pydantic.errors import PathNotExistsError
from pydantic.fields import Field
from graia.application.protocol import UploadMethods

from graia.application.protocol.exceptions import MissingNecessaryOne
from pydantic import validator

from .....context import application, event_loop, image_method
from ...targets.friend import Friend
from ...targets.group import Group, Member
from .. import ExternalElement, InternalElement
from . import external as External


class Plain(InternalElement, ExternalElement):
    type: str = "Plain"
    text: str

    def __init__(self, text, *_, **__) -> NoReturn:
        super().__init__(text=text)

    def toExternal(self) -> "Plain":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "Plain":
        return external_element

    def asDisplay(self) -> str:
        return self.text

class Source(InternalElement, ExternalElement):
    id: int
    time: datetime

    def toExternal(self) -> "Source":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "Source":
        return external_element

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }

class Quote(InternalElement, ExternalElement):
    id: int
    groupId: int
    senderId: int
    targetId: int
    origin: "MessageChain"

    @validator("origin")
    def _(cls, v):
        from graia.application.protocol.entities.message.chain import MessageChain
        return MessageChain.parse_obj(v)

    @classmethod
    def fromExternal(_, external_element) -> "Quote":
        return external_element

class At(InternalElement, ExternalElement):
    type: str = "At"
    target: int
    display: str

    def asDisplay(self) -> str:
        return self.display

    def toExternal(self) -> "At":
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "At":
        return external_element

class AtAll(InternalElement, ExternalElement):
    type: str = "AtAll"

    def asDisplay(self) -> str:
        return "@全体成员"

    def toExternal(self) -> "AtAll":
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "AtAll":
        return external_element

class Face(InternalElement, ExternalElement):
    type: str = "Face"
    faceId: int
    name: str

    def toExternal(self) -> "Face":
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "Face":
        return external_element

class ImageType(Enum):
    Friend = "Friend"
    Group = "Group"
    Unknown = "Unknown"

class Image(InternalElement):
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    type: Optional[ImageType]
    
    @validator("type", always=True)
    def _(cls, v, values) -> ImageType:
        if v:
            return v
        if "imageId" not in values:
            return ImageType.Unknown
        if not values['imageId']:
            return ImageType.Unknown
        if values['imageId'].startswith("/"):
            return ImageType.Friend
        elif values['imageId'].startswith("{") and\
             values['imageId'].endswith("}.mirai"):
            return ImageType.Group
        else:
            return ImageType.Unknown

    def toExternal(self):
        return External.Image(
            imageId=self.imageId,
            url=self.url,
            path=self.path
        )

    @classmethod
    def fromExternal(cls, external_element) -> "Image":
        return cls(
            imageId=external_element.imageId,
            url=external_element.url,
            path=external_element.path
        )
    
    @classmethod
    async def fromLocalFile(cls, filepath: Union[Path, str], method: Optional[UploadMethods] = None) -> "Image":
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError("you should give us a existed file's path")
        app = application.get()
        method = method or image_method.get()
        if not method:
            raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
        return await app.uploadImage(filepath.read_bytes(), method)
        
    @classmethod
    def fromUnsafePath(cls, path: Path) -> "External.Image":
        return External.Image(path=str(path))

    @classmethod
    async def fromUnsafeBytes(cls, image_bytes: bytes, method: Optional[UploadMethods] = None) -> "Image":
        app = application.get()
        method = method or image_method.get()
        if not method:
            raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
        return await app.uploadImage(image_bytes, method.value)

    @classmethod
    def fromUnsafeAddress(cls, url: str) -> "External.Image":
        return External.Image(url=url)

class FlashImage(Image):
    def toExternal(self):
        return External.FlashImage(
            imageId=self.imageId,
            url=self.url,
            path=self.path
        )

    @classmethod
    def fromExternal(cls, external_element) -> "FlashImage":
        return cls(
            imageId=external_element.imageId,
            url=external_element.url,
            path=external_element.path
        )

class Xml(InternalElement, ExternalElement):
    xml: str

class Json(InternalElement, ExternalElement):
    Json: str = Field(..., alias="json")

    def dict(self, *args, **kwargs):
        return super().dict(*args, **({
            **kwargs,
            "by_alias": True
        }))

class App(InternalElement, ExternalElement):
    content: str

class PokeMethods(Enum):
    Poke = "Poke"
    ShowLove = "ShowLove"
    Like = "Like"
    Heartbroken = "Heartbroken"
    SixSixSix = "SixSixSix"
    FangDaZhao = "FangDaZhao"

class Poke(InternalElement, ExternalElement):
    name: PokeMethods

from ..chain import MessageChain

Quote.update_forward_refs(MessageChain=MessageChain)