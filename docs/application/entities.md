Module graia.application.entities
=================================

Classes
-------

`MiraiConfig(**data: Any)`
:   `/config` 接口的序列化实体类
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `cacheSize: int`
    :

    `enableWebsocket: bool`
    :

`UploadMethods(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   用于向 `uploadImage` 或 `uploadVoice` 方法描述图片的上传类型

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Friend`
    :

    `Group`
    :

    `Temp`
    :