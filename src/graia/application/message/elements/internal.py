import asyncio
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn, Optional, Union
import aiohttp

from pydantic.fields import Field
from graia.application.entities import UploadMethods

from ...exceptions import InvaildArgument
from pydantic import validator

from ...context import application, image_method
from . import ExternalElement, InternalElement, ShadowElement
from graia.application.message.elements import external as External
from aiohttp import ClientSession
import json as MJson


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

    def asSerializationString(self) -> str:
        return self.text


class Source(InternalElement, ExternalElement):
    "表示消息在一个特定聊天区域内的唯一标识"
    id: int
    time: datetime

    @classmethod
    def fromExternal(_, external_element) -> "Source":
        return external_element

    def asSerializationString(self) -> str:
        return f"[mirai:source:{self.id},{int(self.time.timestamp())}]"

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

    @validator("origin", pre=True, allow_reuse=True)
    def _(cls, v):
        from ..chain import MessageChain

        return MessageChain.parse_obj(v)

    @classmethod
    def fromExternal(_, external_element) -> "Quote":
        return external_element

    def asSerializationString(self) -> str:
        return f" [mirai:quote:{self.id}]"


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
        return str(self.display) if self.display else f"@{self.target}"

    def toExternal(self) -> "At":
        try:
            if image_method.get() != UploadMethods.Group:
                raise InvaildArgument(
                    "you cannot use this element in this method: {0}".format(
                        image_method.get().value
                    )
                )
        except LookupError:
            pass
        return self

    def asSerializationString(self) -> str:
        return f"[mirai:at:{self.target},{self.display}]"

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
                raise InvaildArgument(
                    "you cannot use this element in this method: {0}".format(
                        image_method.get().value
                    )
                )
        except LookupError:
            pass
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "AtAll":
        return external_element

    def asSerializationString(self) -> str:
        return "[mirai:atall]"


class Face(InternalElement, ExternalElement):
    "表示消息中所附带的表情, 这些表情大多都是聊天工具内置的."
    type: str = "Face"
    faceId: int
    name: Optional[str] = None

    def toExternal(self) -> "Face":
        return self

    @classmethod
    def fromExternal(cls, external_element) -> "Face":
        return external_element

    def asDisplay(self) -> str:
        return "[表情]"

    def asSerializationString(self) -> str:
        return f"[mirai:face:{self.faceId}]"


class ImageType(Enum):
    Friend = "Friend"
    Group = "Group"
    Temp = "Temp"
    Unknown = "Unknown"


image_upload_method_type_map = {
    UploadMethods.Friend: ImageType.Friend,
    UploadMethods.Group: ImageType.Group,
    UploadMethods.Temp: ImageType.Temp,
}


class ShadowImage(InternalElement, ExternalElement, ShadowElement):
    method: Optional[UploadMethods]
    is_flash: bool = False

    def asFlash(self):
        self.is_flash = True
        return self

    def fromExternal(cls, external_element) -> "InternalElement":
        return external_element

    class Config:
        allow_mutation = True


class Image_LocalFile(ShadowImage):
    filepath: Path

    def __init__(self, filepath: Path, method: Optional[UploadMethods] = None) -> None:
        super().__init__(filepath=filepath, method=method)

    async def toExternal(self):
        app = application.get()
        try:
            methodd = self.method or image_method.get()
        except LookupError:
            raise ValueError(
                "you should give the 'method' for upload when you are out of the event receiver."
            )
        if not self.is_flash:
            return await app.uploadImage(
                self.filepath.read_bytes(), methodd, return_external=True
            )
        else:
            return FlashImage.fromExternal(
                await app.uploadImage(
                    self.filepath.read_bytes(), methodd, return_external=True
                )
            ).toExternal()

    async def getReal(self, method: UploadMethods) -> "Image":
        """从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.
        """
        app = application.get()
        return await app.uploadImage(
            self.filepath.read_bytes(), method, return_external=True
        )


class Image_UnsafeBytes(ShadowImage):
    image_bytes: bytes

    def __init__(
        self, image_bytes: bytes, method: Optional[UploadMethods] = None
    ) -> None:
        super().__init__(image_bytes=image_bytes, method=method)

    async def toExternal(self):
        app = application.get()
        try:
            methodd = self.method or image_method.get()
        except LookupError:
            raise ValueError(
                "you should give the 'method' for upload when you are out of the event receiver."
            )
        if not self.is_flash:
            return await app.uploadImage(
                self.image_bytes, methodd, return_external=True
            )
        else:
            return FlashImage.fromExternal(
                await app.uploadImage(self.image_bytes, methodd, return_external=True)
            ).toExternal()

    async def getReal(self, method: UploadMethods) -> "Image":
        """从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.
        """
        app = application.get()
        return await app.uploadImage(self.image_bytes, method)


class Image_NetworkAddress(ShadowImage):
    url: str

    def __init__(self, url: str, method: Optional[UploadMethods] = None) -> None:
        super().__init__(url=url, method=method)

    async def toExternal(self):
        app = application.get()
        try:
            methodd = self.method or image_method.get()
        except LookupError:
            raise ValueError(
                "you should give the 'method' for upload when you are out of the event receiver."
            )

        async with app.session.get(self.url) as response:
            response.raise_for_status()
            if not self.is_flash:
                return await app.uploadImage(
                    await response.read(), methodd, return_external=True
                )
            else:
                return FlashImage.fromExternal(
                    await app.uploadImage(
                        await response.read(), methodd, return_external=True
                    )
                ).toExternal()

    async def getReal(self, method: UploadMethods) -> "Image":
        """从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.
        """
        app = application.get()
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                return await app.uploadImage(await response.read(), method)


class Image(InternalElement):
    "该消息元素用于承载消息中所附带的图片."
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    type: Optional[ImageType]

    @validator("type", always=True, allow_reuse=True)
    def _(cls, v, values) -> ImageType:
        if v:
            return v
        if "imageId" not in values:
            return ImageType.Unknown
        if not values["imageId"]:
            return ImageType.Unknown
        if values["imageId"].startswith("/"):
            if len(values["imageId"]) == 37:
                return ImageType.Friend
            else:
                return ImageType.Temp
        elif values["imageId"].startswith("{") and values["imageId"].endswith(
            "}.mirai"
        ):
            return ImageType.Group
        else:
            return ImageType.Unknown

    async def toExternal(self):
        try:
            want_type = image_upload_method_type_map.get(image_method.get())
            if self.type != want_type and self.url:
                app = application.get()
                image_byte = await self.http_to_bytes()
                return await app.uploadImage(
                    image_byte, image_method.get(), return_external=True
                )
        except LookupError:
            pass
        return External.Image(imageId=self.imageId, url=self.url, path=self.path)

    @classmethod
    def fromExternal(cls, external_element) -> "Image":
        return cls(
            imageId=external_element.imageId,
            url=external_element.url,
            path=external_element.path,
        )

    @classmethod
    def fromLocalFile(
        cls, filepath: Union[Path, str], method: Optional[UploadMethods] = None
    ) -> "Image":
        """从本地文件中创建一个 Shadow Element, 以此在发送时自动上传图片至服务器, 并借此使包含的图片成功发送.

        Args:
            filepath (Union[Path, str]): 需要上传的图片路径, 可以是字符串也可以是 pathlib.Path 实例
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.

        Raises:
            FileNotFoundError: 所描述的图片文件在文件系统中不存在.

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 其包含有一 asFlash 方法,
                可以将当前图片转为闪照形式发送.

        Examples:
        ``` python
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("./image.png")
            # 发闪照则是 Image.fromLocalFile("./flashimage.png").asFlash()
            # 注意: 闪照是也只能是单独一个消息.
        ]))
        ```
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError("you should give us a existed file's path")
        return Image_LocalFile(filepath, method)

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
    def fromUnsafeBytes(
        cls, image_bytes: bytes, method: Optional[UploadMethods] = None
    ) -> "Image":
        """从不保证有效性的 bytes 中创建一个 Shadow Element, 以此在发送时自动作为图片上传至服务器, 并借此使其可能包含的图片成功发送.

        Args:
            image_bytes: (bytes): 任意 bytes, 不保证内部可能的图片的有效性
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 其包含有一 asFlash 方法,
                可以将当前图片转为闪照形式发送.
        """
        return Image_UnsafeBytes(image_bytes, method)

    @classmethod
    def fromNetworkAddress(
        cls, url: str, method: Optional[UploadMethods] = None
    ) -> "Image":
        """从不保证有效性的网络位置中创建一个 Shadow Element, 以此在发送时自动从该指定位置获取并作为图片上传至服务器,
        并借此使其可能包含的图片成功发送.

        Args:
            url: (str): 可以是任意 http/https 的 url, 不保证其有效性, 且可能抛出任意形式的网络错误
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.

        Raises:
            ClientResponseError: HTTP 网络请求错误

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 其包含有一 asFlash 方法,
                可以将当前图片转为闪照形式发送.
        """
        return Image_NetworkAddress(url, method)

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

    def asFlash(self) -> "FlashImage":
        return FlashImage.fromOriginalImage(self)

    def asSerializationString(self) -> str:
        return f"[mirai:image:{self.imageId}]"


class FlashImage(Image, InternalElement):
    """用于承载 QQ 中的特殊消息: 闪照的消息组件.

    通常, 你需要先使用 Image 中提供的各种工厂方法创建一"普通"的 Image 对象, 然后再使用 asFlash 方法将其转换为闪照.
    """

    def toExternal(self):
        return External.FlashImage(imageId=self.imageId, url=self.url, path=self.path)

    @classmethod
    def fromExternal(cls, external_element) -> "FlashImage":
        return cls(
            imageId=external_element.imageId,
            url=external_element.url,
            path=external_element.path,
        )

    @classmethod
    def fromOriginalImage(cls, image_element: Image) -> "FlashImage":
        return cls(
            imageId=image_element.imageId,
            url=image_element.url,
            path=image_element.path,
        )

    def asDisplay(self) -> str:
        return "[闪照]"

    def asNormal(self) -> "Image":
        return Image.fromExternal(self)

    def asSerializationString(self) -> str:
        return f"[mirai:flash:{self.imageId}]"


class VoiceUploadType(Enum):
    Group = "group"
    Unknown = "unknown"


class Voice_LocalFile(ShadowElement, InternalElement, ExternalElement):
    filepath: Path
    method: Optional[UploadMethods]

    def __init__(self, filepath: Path, method: Optional[UploadMethods] = None) -> None:
        super().__init__(filepath=filepath, method=method)

    def fromExternal(cls, external_element) -> "InternalElement":
        return external_element

    async def toExternal(self):
        app = application.get()
        try:
            methodd = self.method or image_method.get()
        except LookupError:
            raise ValueError(
                "you should give the 'method' for upload when you are out of the event receiver."
            )

        return await app.uploadVoice(
            self.filepath.read_bytes(), methodd, return_external=True
        )

    async def getReal(self, method: UploadMethods) -> "Image":
        """从本 Shadow Element 中生成一真正的 Voice 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Voice: 所生成的, 真正的 Voice 对象.
        """
        app = application.get()
        return await app.uploadVoice(
            self.filepath.read_bytes(), method, return_external=True
        )


class Voice(InternalElement):
    voiceId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    type: Optional[VoiceUploadType]

    def toExternal(self):
        return External.Voice(voiceId=self.voiceId, url=self.url, path=self.path)

    @classmethod
    def fromExternal(cls, external_element) -> "Voice":
        return cls(
            voiceId=external_element.voiceId,
            url=external_element.url,
            path=external_element.path,
        )

    def asSerializationString(self) -> str:
        return f"[mirai:voice:{self.voiceId}]"

    def asDisplay(self) -> str:
        return "[语音]"

    @validator("type", always=True, allow_reuse=True)
    def _(cls, v, values) -> VoiceUploadType:
        if v:
            return v
        if "voiceId" not in values:
            return VoiceUploadType.Unknown
        if not values["voiceId"]:
            return VoiceUploadType.Unknown
        if values["voiceId"]:
            return VoiceUploadType.Group  # mirai 当前版本只支持群语音.

    def fromLocalFile(
        self, filepath: Union[str, Path], method: Optional[UploadMethods] = None
    ) -> "Voice":
        """从本地文件中创建一个 Shadow Element, 以此在发送时自动上传语音至服务器, 并借此使包含的语音成功发送.

        Args:
            filepath (Union[Path, str]): 需要上传的图片路径, 可以是字符串也可以是 pathlib.Path 实例
            method (Optional[UploadMethods], default = None): 语音上传时使用的方法, 通常可以使程序自行判定.

        Raises:
            FileNotFoundError: 所描述的语音文件在文件系统中不存在.

        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Voice 特征属性的叠加态消息元素
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError("you should give us a existed file's path")
        return Voice_LocalFile(filepath, method)


class Xml(InternalElement, ExternalElement):
    type = "Xml"
    xml: str

    def __init__(self, xml, *_, **__) -> None:
        super().__init__(xml=xml)

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

    def __init__(self, json: Union[dict, str], *_, **__) -> None:
        if isinstance(json, dict):
            json = MJson.dumps(json)
        super().__init__(json=json)

    def dict(self, *args, **kwargs):
        return super().dict(*args, **({**kwargs, "by_alias": True}))

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
