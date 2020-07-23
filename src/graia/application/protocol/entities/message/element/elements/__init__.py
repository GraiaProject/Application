import asyncio
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Union

from pydantic.errors import PathNotExistsError
from graia.application.protocol import UploadMethods

from graia.application.protocol.exceptions import MissingNecessaryOne
from pydantic import validator

from ......context import application, event_loop, image_method
from ....targets.friend import Friend
from ....targets.group import Group, Member
from .. import ExternalElement, InternalElement
from ..chain import MessageChain
from . import external as External


class Plain(InternalElement, ExternalElement):
    text: str

    def __init__(self, text) -> NoReturn:
        self.text = text

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

class Quote(InternalElement):
    id: str
    group: Optional[Group] = None
    sender: Union[Member, Friend]
    target: Union[Group, Friend]
    originMessage: MessageChain
    
    @classmethod
    async def fromExternal(cls, external_element: External.Quote) -> "Quote":
        app = application.get()
        return cls(
            group=await app.getGroup(external_element.groupId)
             if external_element.groupId != 0 else None,
            sender=await app.getMember(
                external_element.groupId,
                external_element.senderId
            ) if external_element.groupId != 0 else \
                await app.getFriend(external_element.senderId),
            target=await app.getGroup(
                external_element.groupId
            ) if external_element.groupId != 0 else \
                await app.getFriend(external_element.senderId),
            originMessage=external_element.origin
        )

class At(InternalElement, ExternalElement):
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
    def asDisplay(self) -> str:
        return "@全体成员"

    def toExternal(self) -> "AtAll":
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "AtAll":
        return external_element

class Face(InternalElement, ExternalElement):
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
    type: ImageType
    
    @validator("type", always=True)
    def _(cls, v, values) -> ImageType:
        if v:
            return v
        if "imageId" not in values:
            return ImageType.Unknown
        if values['imageId'].startswith("/"):
            return ImageType.Friend
        elif values['imageId'].startswith("{") and\
             values['imageId'].endswith("}.mirai"):
            return ImageType.Group
        else:
            return ImageType.Unknown

    @validator("imageId", "url", "path")
    def _(cls, v):
        if not any(v):
            raise MissingNecessaryOne("One of the following fields must be provided: imageId, url or path")

    def toExternal(self) -> External.Image:
        return External.Image(
            imageId=self.imageId,
            url=self.url,
            path=self.path
        )

    @classmethod
    def fromExternal(cls, external_element: External.Image) -> "Image":
        return cls(
            imageId=external_element.imageId,
            url=external_element.url,
            path=external_element.path
        )
    
    @classmethod
    async def fromLocalFile(cls, filepath: Path, method: Optional[UploadMethods] = None) -> "Image":
        if not filepath.exists():
            raise FileNotFoundError("you should give us a existed file's path")
        app = application.get()
        method = method or image_method.get()
        if not method:
            raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
        return await app.uploadImage(filepath.read_bytes(), method.value)
        
    @classmethod
    async def fromUnsafePath(cls, path: Path) -> "Image":
        return cls(path=str(path))

    @classmethod
    async def fromUnsafeBytes(cls, image_bytes: bytes, method: Optional[UploadMethods] = None) -> "Image":
        app = application.get()
        method = method or image_method.get()
        if not method:
            raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
        return await app.uploadImage(image_bytes, method.value)

    @classmethod
    async def fromUnsafeAddress(cls, url: str) -> "Image":
        return cls(url=url)

class FlashImage(Image):
    pass

class Xml(InternalElement, ExternalElement):
    xml: str

class Json(InternalElement, ExternalElement):
    json: str

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