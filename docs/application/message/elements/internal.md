Module graia.application.message.elements.internal
==================================================

Classes
-------

`App(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `content: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

`At(target: int, **kwargs)`
:   该消息元素用于承载消息中用于提醒/呼唤特定用户的部分.
    
    实例化一个 At 消息元素, 用于承载消息中用于提醒/呼唤特定用户的部分.
    
    Args:
        target (int): 需要提醒/呼唤的特定用户的 QQ 号(或者说 id.)

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `display: Union[str, NoneType]`
    :

    `target: int`
    :

    `type: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

`AtAll(**data: Any)`
:   该消息元素用于群组中的管理员提醒群组中的所有成员
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `type: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

`Face(**data: Any)`
:   表示消息中所附带的表情, 这些表情大多都是聊天工具内置的.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `faceId: int`
    :

    `name: Union[str, NoneType]`
    :

    `type: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

`FlashImage(**data: Any)`
:   用于承载 QQ 中的特殊消息: 闪照的消息组件.
    
    通常, 你需要先使用 Image 中提供的各种工厂方法创建一"普通"的 Image 对象, 然后再使用 asFlash 方法将其转换为闪照.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.internal.Image
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `imageId: Union[str, NoneType]`
    :

    `path: Union[str, NoneType]`
    :

    `type: Union[graia.application.message.elements.internal.ImageType, NoneType]`
    :

    `url: Union[str, NoneType]`
    :

    ### Static methods

    `fromOriginalImage(image_element: graia.application.message.elements.internal.Image) ‑> graia.application.message.elements.internal.FlashImage`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asNormal(self) ‑> graia.application.message.elements.internal.Image`
    :

    `asSerializationString(self) ‑> str`
    :

`Image(**data: Any)`
:   该消息元素用于承载消息中所附带的图片.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Descendants

    * graia.application.message.elements.internal.FlashImage

    ### Class variables

    `imageId: Union[str, NoneType]`
    :

    `path: Union[str, NoneType]`
    :

    `type: Union[graia.application.message.elements.internal.ImageType, NoneType]`
    :

    `url: Union[str, NoneType]`
    :

    ### Static methods

    `fromLocalFile(filepath: Union[pathlib.Path, str], method: Union[graia.application.entities.UploadMethods, NoneType] = None) ‑> graia.application.message.elements.internal.Image`
    :   从本地文件中创建一个 Shadow Element, 以此在发送时自动上传图片至服务器, 并借此使包含的图片成功发送.
        
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

    `fromNetworkAddress(url: str, method: Union[graia.application.entities.UploadMethods, NoneType] = None) ‑> graia.application.message.elements.internal.Image`
    :   从不保证有效性的网络位置中创建一个 Shadow Element, 以此在发送时自动从该指定位置获取并作为图片上传至服务器,
        并借此使其可能包含的图片成功发送.
        
        Args:
            url: (str): 可以是任意 http/https 的 url, 不保证其有效性, 且可能抛出任意形式的网络错误
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.
        
        Raises:
            ClientResponseError: HTTP 网络请求错误
        
        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 其包含有一 asFlash 方法,
                可以将当前图片转为闪照形式发送.

    `fromUnsafeAddress(url: str) ‑> graia.application.message.elements.external.Image`
    :

    `fromUnsafeBytes(image_bytes: bytes, method: Union[graia.application.entities.UploadMethods, NoneType] = None) ‑> graia.application.message.elements.internal.Image`
    :   从不保证有效性的 bytes 中创建一个 Shadow Element, 以此在发送时自动作为图片上传至服务器, 并借此使其可能包含的图片成功发送.
        
        Args:
            image_bytes: (bytes): 任意 bytes, 不保证内部可能的图片的有效性
            method (Optional[UploadMethods], default = None): 图片上传时使用的方法, 通常可以使程序自行判定.
        
        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Image 特征属性的叠加态消息元素; 其包含有一 asFlash 方法,
                可以将当前图片转为闪照形式发送.

    `fromUnsafePath(path: Union[pathlib.Path, str]) ‑> graia.application.message.elements.external.Image`
    :   不检查路径安全性, 直接实例化元素, 让 mirai-api-http 自行读取图片文件.
        
        Args:
            path (Union[Path, str]): 图片文件路径
        
        Returns:
            Image: 作为外部态存在的 Image 消息元素

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asFlash(self) ‑> graia.application.message.elements.internal.FlashImage`
    :

    `asSerializationString(self) ‑> str`
    :

    `http_to_bytes(self, url: str = None) ‑> bytes`
    :   从远端服务器获取图片的 bytes, 注意, 你无法获取并不包含 url 属性的本元素的 bytes.
        
        Args:
            url (str, optional): 如果提供, 则从本参数获取 bytes. 默认为 None.
        
        Raises:
            ValueError: 你尝试获取并不包含 url 属性的本元素的 bytes.
        
        Returns:
            bytes: 图片原始数据

`ImageType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Friend`
    :

    `Group`
    :

    `Temp`
    :

    `Unknown`
    :

`Image_LocalFile(filepath: pathlib.Path, method: Union[graia.application.entities.UploadMethods, NoneType] = None)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.ShadowElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `filepath: pathlib.Path`
    :

    ### Methods

    `getReal(self, method: graia.application.entities.UploadMethods) ‑> graia.application.message.elements.internal.Image`
    :   从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.

`Image_NetworkAddress(url: str, method: Union[graia.application.entities.UploadMethods, NoneType] = None)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.ShadowElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `url: str`
    :

    ### Methods

    `getReal(self, method: graia.application.entities.UploadMethods) ‑> graia.application.message.elements.internal.Image`
    :   从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.

`Image_UnsafeBytes(image_bytes: bytes, method: Union[graia.application.entities.UploadMethods, NoneType] = None)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.ShadowElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `image_bytes: bytes`
    :

    ### Methods

    `getReal(self, method: graia.application.entities.UploadMethods) ‑> graia.application.message.elements.internal.Image`
    :   从本 Shadow Element 中生成一真正的 Image 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Image: 所生成的, 真正的 Image 对象.

`Json(json: Union[dict, str], *_, **__)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `Json: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `dict(self, *args, **kwargs)`
    :   Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

`Plain(text: str, *_, **__)`
:   实例化一个 Plain 消息元素, 用于承载消息中的文字.
    
    Args:
        text (str): 元素所包含的文字

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `text: str`
    :

    `type: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

`Poke(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `name: graia.application.message.elements.internal.PokeMethods`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

`PokeMethods(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `FangDaZhao`
    :

    `Heartbroken`
    :

    `Like`
    :

    `Poke`
    :

    `ShowLove`
    :

    `SixSixSix`
    :

`Quote(**data: Any)`
:   表示消息中回复其他消息/用户的部分, 通常包含一个完整的消息链(`origin` 属性)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `groupId: int`
    :

    `id: int`
    :

    `origin: graia.application.message.chain.MessageChain`
    :

    `senderId: int`
    :

    `targetId: int`
    :

    ### Methods

    `asSerializationString(self) ‑> str`
    :

`ShadowImage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.ShadowElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Descendants

    * graia.application.message.elements.internal.Image_LocalFile
    * graia.application.message.elements.internal.Image_NetworkAddress
    * graia.application.message.elements.internal.Image_UnsafeBytes

    ### Class variables

    `Config`
    :

    `is_flash: bool`
    :

    `method: Union[graia.application.entities.UploadMethods, NoneType]`
    :

    ### Methods

    `asFlash(self)`
    :

`Source(**data: Any)`
:   表示消息在一个特定聊天区域内的唯一标识
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `Config`
    :

    `id: int`
    :

    `time: datetime.datetime`
    :

    ### Methods

    `asSerializationString(self) ‑> str`
    :

`Voice(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `path: Union[str, NoneType]`
    :

    `type: Union[graia.application.message.elements.internal.VoiceUploadType, NoneType]`
    :

    `url: Union[str, NoneType]`
    :

    `voiceId: Union[str, NoneType]`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

    `fromLocalFile(self, filepath: Union[str, pathlib.Path], method: Union[graia.application.entities.UploadMethods, NoneType] = None) ‑> graia.application.message.elements.internal.Voice`
    :   从本地文件中创建一个 Shadow Element, 以此在发送时自动上传语音至服务器, 并借此使包含的语音成功发送.
        
        Args:
            filepath (Union[Path, str]): 需要上传的图片路径, 可以是字符串也可以是 pathlib.Path 实例
            method (Optional[UploadMethods], default = None): 语音上传时使用的方法, 通常可以使程序自行判定.
        
        Raises:
            FileNotFoundError: 所描述的语音文件在文件系统中不存在.
        
        Returns:
            [Shadow Element]: 返回值为一合法, 但不包括任何 Voice 特征属性的叠加态消息元素

`VoiceUploadType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Group`
    :

    `Unknown`
    :

`Voice_LocalFile(filepath: pathlib.Path, method: Union[graia.application.entities.UploadMethods, NoneType] = None)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.ShadowElement
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `filepath: pathlib.Path`
    :

    `method: Union[graia.application.entities.UploadMethods, NoneType]`
    :

    ### Methods

    `getReal(self, method: graia.application.entities.UploadMethods) ‑> graia.application.message.elements.internal.Image`
    :   从本 Shadow Element 中生成一真正的 Voice 对象.
        Args:
            method (UploadMethods): 所需求的图片的上传类型, 具体请阅读 UploadMethods 的相关文档.
        Raises:
            ClientResponseError: HTTP 网络请求错误
        Returns:
            Voice: 所生成的, 真正的 Voice 对象.

`Xml(xml, *_, **__)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `xml: str`
    :

    ### Methods

    `asDisplay(self) ‑> str`
    :