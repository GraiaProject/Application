Module graia.application.exceptions
===================================

Classes
-------

`AccountMuted(*args, **kwargs)`
:   账号在对象所在聊天区域被封禁.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`AccountNotFound(*args, **kwargs)`
:   未能使用所配置的账号激活 sessionKey, 请检查 connect_info 配置.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`ConflictItem(*args, **kwargs)`
:   项冲突/其中一项被重复定义

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`DeprecatedImpl(*args, **kwargs)`
:   该接口已弃用.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`EntangledSuperposition(*args, **kwargs)`
:   你传入的一个 List[InternalElement] 中包含了一个没有重写 toExternal 的消息元素

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`InvaildArgument(*args, **kwargs)`
:   操作参数不合法, 请报告问题.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`InvaildAuthkey(*args, **kwargs)`
:   无效的 authKey 或其配置.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`InvaildSession(*args, **kwargs)`
:   无效的 sessionKey, 请重新获取.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`InvalidEventTypeDefinition(*args, **kwargs)`
:   不合法的事件类型定义.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`MissingNecessaryOne(*args, **kwargs)`
:   应在所提到的参数之中至少传入/使用一个

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`NotSupportedVersion(*args, **kwargs)`
:   该版本不支持本接口.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`TooLongMessage(*args, **kwargs)`
:   消息过长, 尝试分段发送或报告问题.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`UnauthorizedSession(*args, **kwargs)`
:   尚未验证/绑定的 session.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`UnknownTarget(*args, **kwargs)`
:   对象位置未知, 不存在或不可及.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException