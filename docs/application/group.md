Module graia.application.group
==============================

Classes
-------

`Group(**data: Any)`
:   描述 Tencent QQ 中的可发起聊天区域 '群组(group)' 的能被获取到的信息.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `accountPerm: graia.application.group.MemberPerm`
    :

    `id: int`
    :

    `name: str`
    :

`GroupConfig(**data: Any)`
:   描述群组各项功能的设置.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Config`
    :

    `allowMemberInvite: Union[bool, NoneType]`
    :

    `announcement: Union[str, NoneType]`
    :

    `anonymousChat: Union[bool, NoneType]`
    :

    `autoApprove: Union[bool, NoneType]`
    :

    `confessTalk: Union[bool, NoneType]`
    :

    `name: Union[str, NoneType]`
    :

`Member(**data: Any)`
:   描述用户在群组中所具备的有关状态, 包括所在群组, 群中昵称, 所具备的权限, 唯一ID.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `group: graia.application.group.Group`
    :

    `id: int`
    :

    `name: str`
    :

    `permission: graia.application.group.MemberPerm`
    :

`MemberInfo(**data: Any)`
:   描述群组成员的可修改状态, 修改需要管理员/群主权限.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Config`
    :

    `name: Union[str, NoneType]`
    :

    `specialTitle: Union[str, NoneType]`
    :

`MemberPerm(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   描述群成员在群组中所具备的权限

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Administrator`
    :

    `Member`
    :

    `Owner`
    :