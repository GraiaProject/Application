import asyncio
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Text, Union

from pydantic.errors import PathNotExistsError
from pydantic.fields import Field
from graia.application.protocol import UploadMethods

from ....exceptions import InvaildArgument
from pydantic import validator

from .....context import application, image_method
from ...targets.friend import Friend
from ...targets.group import Group, Member
from .. import ExternalElement, InternalElement
from . import external as External
from functools import partial
from aiohttp import ClientSession


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
        try:
            if image_method.get() != UploadMethods.Group:
                raise InvaildArgument("you cannot use this element in this method: {0}".format(image_method.get().value))
        except LookupError:
            pass
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "At":
        return external_element

class AtAll(InternalElement, ExternalElement):
    type: str = "AtAll"

    def asDisplay(self) -> str:
        return "@全体成员"

    def toExternal(self) -> "AtAll":
        try:
            if image_method.get() != UploadMethods.Group:
                raise InvaildArgument("you cannot use this element in this method: {0}".format(image_method.get().value))
        except LookupError:
            pass
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

    def asDisplay(self) -> str:
        return "[表情]"

class ImageType(Enum):
    Friend = "Friend"
    Group = "Group"
    Temp = "Temp"
    Unknown = "Unknown"

image_upload_method_type_map = {
    UploadMethods.Friend: ImageType.Friend,
    UploadMethods.Group: ImageType.Group,
    UploadMethods.Temp: ImageType.Temp
}

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
            if len(values['imageId']) == 37:
                return ImageType.Friend
            else:
                return ImageType.Temp
        elif values['imageId'].startswith("{") and\
             values['imageId'].endswith("}.mirai"):
            return ImageType.Group
        else:
            return ImageType.Unknown

    async def toExternal(self):
        # TODO: 自动图片类型转换
        try:
            want_type = image_upload_method_type_map.get(image_method.get())
            if self.type != want_type and self.url:
                app = application.get()
                image_byte = await self.http_to_bytes()
                return await app.uploadImage(image_byte, image_method.get(), return_external=True)
        except LookupError:
            pass
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
    def fromLocalFile(cls, filepath: Union[Path, str], method: Optional[UploadMethods] = None) -> "Image":
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError("you should give us a existed file's path")
        # 定义魔法闭包类
        class _Image_Internal(InternalElement, ExternalElement):
            @property
            def toExternal(self):
                app = application.get()
                try:
                    methodd = method or image_method.get()
                except LookupError:
                    raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
                return partial(app.uploadImage, filepath.read_bytes(), methodd, return_external=True)

            def fromExternal(cls, external_element) -> "InternalElement":
                return external_element
        return _Image_Internal()

    @classmethod
    def fromUnsafePath(cls, path: Path) -> "External.Image":
        return External.Image(path=str(path))

    @classmethod
    async def fromUnsafeBytes(cls, image_bytes: bytes, method: Optional[UploadMethods] = None) -> "Image":
        if not method:
            raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
        class _Image_Internal(InternalElement, ExternalElement):
            @property
            def toExternal(self):
                app = application.get()
                try:
                    methodd = method or image_method.get()
                except LookupError:
                    raise ValueError("you should give the 'method' for upload when you are out of the event receiver.")
                return partial(app.uploadImage, image_bytes, methodd, return_external=True)

            def fromExternal(cls, external_element) -> "InternalElement":
                return external_element
        return _Image_Internal()

    @classmethod
    def fromUnsafeAddress(cls, url: str) -> "External.Image":
        return External.Image(url=url)
    
    def asDisplay(self) -> str:
        return "[图片]"
    
    async def http_to_bytes(self, url=None) -> bytes:
        if not (self.url or url):
            raise ValueError("you should offer a url.")
        async with ClientSession() as session:
            async with session.get(self.url or url) as response:
                response.raise_for_status()
                return await response.read()

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

    def asDisplay(self) -> str:
        return "[闪照]"

class Xml(InternalElement, ExternalElement):
    xml: str

    def asDisplay(self) -> str:
        return "[XML消息]"

class Json(InternalElement, ExternalElement):
    Json: str = Field(..., alias="json")

    def dict(self, *args, **kwargs):
        return super().dict(*args, **({
            **kwargs,
            "by_alias": True
        }))

    def asDisplay(self) -> str:
        return "[JSON消息]"

class App(InternalElement, ExternalElement):
    content: str

    def asDisplay(self) -> str:
        return "[APP消息]"

class PokeMethods(Enum):
    Poke = "Poke"
    ShowLove = "ShowLove"
    Like = "Like"
    Heartbroken = "Heartbroken"
    SixSixSix = "SixSixSix"
    FangDaZhao = "FangDaZhao"

class Poke(InternalElement, ExternalElement):
    name: PokeMethods

    def asDisplay(self) -> str:
        return "[戳一戳:{0}]".format(self.name)

from ..chain import MessageChain

Quote.update_forward_refs(MessageChain=MessageChain)