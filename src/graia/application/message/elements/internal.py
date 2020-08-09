import asyncio
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Union

from pydantic.fields import Field
from graia.application.entities import UploadMethods

from ...exceptions import InvaildArgument
from pydantic import validator

from ...context import application, image_method
from . import ExternalElement, InternalElement
from . import external as External
from functools import partial
from aiohttp import ClientSession


class Plain(InternalElement, ExternalElement):
    type: str = "Plain"
    text: str

    def __init__(self, text: str, *_, **__) -> NoReturn:
        """实例化一个 Plain 消息元素, 用于承载消息中的文字.

        Args:
            text (str): 元素所包含的文字
        """
        super().__init__(text=text)

    def toExternal(self) -> "Plain":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "Plain":
        return external_element

    def asDisplay(self) -> str:
        return self.text

class Source(InternalElement, ExternalElement):
    "表示消息在一个特定聊天区域内的唯一标识"
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
    "表示消息中回复其他消息/用户的部分, 通常包含一个完整的消息链(`origin` 属性)"
    id: int
    groupId: int
    senderId: int
    targetId: int
    origin: "MessageChain"

    @validator("origin", pre=True)
    def _(cls, v):
        from ..chain import MessageChain
        return MessageChain.parse_obj(v)

    @classmethod
    def fromExternal(_, external_element) -> "Quote":
        return external_element

class At(InternalElement, ExternalElement):
    """该消息元素用于承载消息中用于提醒/呼唤特定用户的部分."""
    type: str = "At"
    target: int
    display: Optional[str] = None

    def __init__(self, target: int, **kwargs) -> None:
        """实例化一个 At 消息元素, 用于承载消息中用于提醒/呼唤特定用户的部分.

        Args:
            target (int): 需要提醒/呼唤的特定用户的 QQ 号(或者说 id.)
        """
        super().__init__(target=target, **kwargs)

    def asDisplay(self) -> str:
        return str(self.display)

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
    "该消息元素用于群组中的管理员提醒群组中的所有成员"
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
    "表示消息中所附带的表情, 这些表情大多都是聊天工具内置的."
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
    "该消息元素用于承载消息中所附带的图片. 你可以自由使用该元素."
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
        """从本地文件中创建一个 Shadow Element, 以此在发送时自动上传图片至服务器, 并借此使包含的图片成功发送.

        Args:
            filepath (Union[Path, str]): 需要上传的图片路径, 可以是字符串也可以是 pathlib.Path 实例
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.

        Raises:
            FileNotFoundError: 所描述的图片文件在文件系统中不存在.

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 你无需了解这到底有什么魔法.
        """
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
    def fromUnsafePath(cls, path: Union[Path, str]) -> "External.Image":
        """不检查路径安全性, 直接实例化元素, 让 mirai-api-http 自行读取图片文件.

        Args:
            path (Union[Path, str]): 图片文件路径

        Returns:
            Image: 作为外部态存在的 Image 消息元素
        """
        return External.Image(path=str(path))

    @classmethod
    async def fromUnsafeBytes(cls, image_bytes: bytes, method: Optional[UploadMethods] = None) -> "Image":
        """从不保证有效性的 bytes 中创建一个 Shadow Element, 以此在发送时自动作为图片上传至服务器, 并借此使其可能包含的图片成功发送.

        Args:
            image_bytes: (bytes): 任意 bytes, 不保证内部可能的图片的有效性
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 你无需了解这到底有什么魔法.
        """
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
    
    async def http_to_bytes(self, url: str = None) -> bytes:
        """从远端服务器获取图片的 bytes, 注意, 你无法获取并不包含 url 属性的本元素的 bytes.

        Args:
            url (str, optional): 如果提供, 则从本参数获取 bytes. 默认为 None.

        Raises:
            ValueError: 你尝试获取并不包含 url 属性的本元素的 bytes.

        Returns:
            bytes: 图片原始数据
        """
        if not (self.url or url):
            raise ValueError("you should offer a url.")
        async with ClientSession() as session:
            async with session.get(self.url or url) as response:
                response.raise_for_status()
                return await response.read()

class FlashImage(Image, InternalElement):
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

    @classmethod
    def fromOriginalImage(cls, image_element: Image) -> "FlashImage":
        return cls(
            imageId=image_element.imageId,
            url=image_element.url,
            path=image_element.path
        )

    def asDisplay(self) -> str:
        return "[闪照]"

class Xml(InternalElement, ExternalElement):
    type = "Xml"
    xml: str

    def toExternal(self):
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "Xml":
        return external_element

    def asDisplay(self) -> str:
        return "[XML消息]"

class Json(InternalElement, ExternalElement):
    type = "Json"
    Json: str = Field(..., alias="json")

    def dict(self, *args, **kwargs):
        return super().dict(*args, **({
            **kwargs,
            "by_alias": True
        }))

    def asDisplay(self) -> str:
        return "[JSON消息]"
    
    def toExternal(self) -> "Json":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "Json":
        return external_element

class App(InternalElement, ExternalElement):
    type = "App"
    content: str

    def asDisplay(self) -> str:
        return "[APP消息]"
    
    def toExternal(self) -> "App":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "App":
        return external_element

class PokeMethods(Enum):
    Poke = "Poke"
    ShowLove = "ShowLove"
    Like = "Like"
    Heartbroken = "Heartbroken"
    SixSixSix = "SixSixSix"
    FangDaZhao = "FangDaZhao"

class Poke(InternalElement, ExternalElement):
    type = "Poke"
    name: PokeMethods

    def asDisplay(self) -> str:
        return "[戳一戳:{0}]".format(self.name)
    
    def toExternal(self) -> "Poke":
        return self
    
    @classmethod
    def fromExternal(_, external_element) -> "Poke":
        return external_element

from ..chain import MessageChain

Quote.update_forward_refs(MessageChain=MessageChain)