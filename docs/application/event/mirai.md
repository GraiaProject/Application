Module graia.application.event.mirai
====================================

Classes
-------

`BotGroupPermissionChangeEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号在一特定群组内所具有的权限发生变化
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: graia.application.group.MemberPerm`
    :

    `group: graia.application.group.Group`
    :

    `origin: graia.application.group.MemberPerm`
    :

    `type: str`
    :

`BotInvitedJoinGroupRequestEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号接受到来自某个账号的邀请加入某个群组的请求.
    
    ** 注意: 当监听该事件时, 请使用原始事件类作为类型注解, 以此获得事件类实例, 并执行相关操作. **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Addon Introduction:
        该事件的处理需要你获取原始事件实例.
        1. 读取该事件的基础信息:
        ``` python
        event.supplicant: int # 邀请所辖账号加入群组的用户的 ID
        event.groupId: Optional[int] # 对方邀请所辖账号加入的群组的 ID
        event.groupName: str # 对方邀请所辖账号加入的群组的名称
        event.nickname: str # 对方的昵称
        event.message: str # 对方发起请求时填写的描述
        ```
    
        2. 同意请求: `await event.accept()`, 具体查看该方法所附带的说明.
        3. 拒绝请求: `await event.reject()`, 具体查看该方法所附带的说明.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `groupId: Union[int, NoneType]`
    :

    `groupName: str`
    :

    `message: str`
    :

    `nickname: str`
    :

    `requestId: int`
    :

    `supplicant: int`
    :

    `type: str`
    :

    ### Methods

    `accept(self, message: str = '') ‑> NoReturn`
    :   接受邀请并加入群组/发起对指定群组的加入申请.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `reject(self, message: str = '') ‑> NoReturn`
    :   拒绝对方加入指定群组的邀请.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

`BotJoinGroupEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号加入指定群组
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation, optional = None): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `group: graia.application.group.Group`
    :

    `type: str`
    :

`BotLeaveEventActive(**data: Any)`
:   当该事件发生时, 应用实例所辖账号主动退出了某群组.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation, optional = None): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `group: graia.application.group.Group`
    :

    `type: str`
    :

`BotLeaveEventKick(**data: Any)`
:   当该事件发生时, 应用实例所辖账号被某群组的管理员/群主从该群组中删除.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation, optional = None): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `group: graia.application.group.Group`
    :

    `type: str`
    :

`BotMuteEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号在一特定群组内被管理员/群主禁言
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Member (annotation, optional = None): 执行禁言操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
        Group (annotation, optional = None): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `durationSeconds: int`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `type: str`
    :

`BotOfflineEventActive(**data: Any)`
:   当该事件发生时, 应用实例所辖账号主动离线
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `qq: int`
    :

    `type: str`
    :

`BotOfflineEventDropped(**data: Any)`
:   当该事件发生时, 应用实例所辖账号与服务器的连接被服务器主动断开, 或因网络原因离线
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `qq: int`
    :

    `type: str`
    :

`BotOfflineEventForce(**data: Any)`
:   当该事件发生时, 应用实例所辖账号被迫离线
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `qq: int`
    :

    `type: str`
    :

`BotOnlineEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号登录成功
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `qq: int`
    :

    `type: str`
    :

`BotReloginEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号正尝试重新登录
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `qq: int`
    :

    `type: str`
    :

`BotUnmuteEvent(**data: Any)`
:   当该事件发生时, 应用实例所辖账号在一特定群组内被管理员/群主解除禁言
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Member (annotation, optional = None): 执行解除禁言操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
        Group (annotation, optional = None): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `type: str`
    :

`FriendRecallEvent(**data: Any)`
:   当该事件发生时, 有一位与应用实例所辖账号为好友关系的用户撤回了一条消息
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `authorId: int`
    :

    `messageId: int`
    :

    `operator: int`
    :

    `time: int`
    :

    `type: str`
    :

`GroupAllowAnonymousChatEvent(**data: Any)`
:   该事件发生时, 有一群组修改了有关匿名聊天的相关设定
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 修改了相关设定的群组
        Member (annotation, return:optional): 作出此操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: bool`
    :

    `group: graia.application.group.Group`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: bool`
    :

    `type: str`
    :

`GroupAllowConfessTalkEvent(**data: Any)`
:   该事件发生时, 有一群组修改了有关坦白说的相关设定
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 修改了相关设定的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: bool`
    :

    `group: graia.application.group.Group`
    :

    `isByBot: bool`
    :

    `origin: bool`
    :

    `type: str`
    :

`GroupAllowMemberInviteEvent(**data: Any)`
:   该事件发生时, 有一群组修改了有关是否允许已有成员邀请其他用户加入群组的相关设定
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 修改了相关设定的群组
        Member (annotation, return:optional): 作出此操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: bool`
    :

    `group: graia.application.group.Group`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: bool`
    :

    `type: str`
    :

`GroupEntranceAnnouncementChangeEvent(**data: Any)`
:   该事件发生时, 有一群组被修改了入群公告
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 被修改了入群公告的群组
        Member (annotation, return:optional): 作出此操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: str`
    :

    `group: graia.application.group.Group`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: str`
    :

    `type: str`
    :

`GroupMuteAllEvent(**data: Any)`
:   该事件发生时, 有一群组开启了全体禁言
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 开启了全体禁言的群组
        Member (annotation, return:optional): 作出此操作的管理员/群主, 若为 None 则为应用实例所辖账号操作
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: bool`
    :

    `group: graia.application.group.Group`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: bool`
    :

    `type: str`
    :

`GroupNameChangeEvent(**data: Any)`
:   该事件发生时, 有一群组被修改了群名称
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 被修改了群名称的群组
        Member (annotation): 更改群名称的成员, 权限必定为管理员或是群主
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: str`
    :

    `group: graia.application.group.Group`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: str`
    :

    `type: str`
    :

`GroupRecallEvent(**data: Any)`
:   当该事件发生时, 有群成员在指定群组撤回了一条消息, 注意, 这里的群成员若具有管理员/群主权限, 则他们可以撤回其他普通群员的消息, 且不受发出时间限制.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Member (annotation, return:optional): 执行本操作的群成员, 若为 None 则为应用实例所辖账号操作
        Group (annotation): 发生该事件的群组
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `authorId: int`
    :

    `group: graia.application.group.Group`
    :

    `messageId: int`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `time: datetime.datetime`
    :

    `type: str`
    :

`MemberCardChangeEvent(**data: Any)`
:   该事件发生时, 有一群组成员的群名片被更改, 执行者可能是管理员/群主, 该成员自己, 也可能是应用实例所辖账号(这时, `operator` 为 `None`).
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生该事件的群组
        Member (annotation):
          - `"target"` (default, const, str): 被更改群名片的成员
          - `"operator"` (default, const, str, return:optional): 该操作的执行者, 可能是管理员/群主, 该成员自己, 也可能是应用实例所辖账号(这时, `operator` 为 `None`).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: str`
    :

    `member: graia.application.group.Member`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `origin: str`
    :

    `type: str`
    :

`MemberJoinEvent(**data: Any)`
:   该事件发生时, 有一新成员加入了一特定群组
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 该用户加入的群组
        Member (annotation): 关于该用户的成员实例
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `member: graia.application.group.Member`
    :

    `type: str`
    :

`MemberJoinRequestEvent(**data: Any)`
:   当该事件发生时, 有一用户向机器人作为管理员/群主的群组申请加入群组.
    
    ** 注意: 当监听该事件时, 请使用原始事件类作为类型注解, 以此获得事件类实例, 并执行相关操作. **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Addon Introduction:
        该事件的处理需要你获取原始事件实例.
        1. 读取该事件的基础信息:
        ``` python
        event.supplicant: int # 申请加入群组的用户的 ID
        event.groupId: Optional[int] # 对方试图加入的群组的 ID
        event.groupName: str # 对方试图加入的群组的名称
        event.nickname: str # 对方的昵称
        event.message: str # 对方发起请求时填写的描述
        ```
    
        2. 同意请求: `await event.accept()`, 具体查看该方法所附带的说明.
        3. 拒绝请求: `await event.reject()`, 具体查看该方法所附带的说明.
        4. 忽略请求: `await event.ignore()`, 具体查看该方法所附带的说明.
        5. 拒绝并不再接受来自对方的请求: `await event.rejectAndBlock()`, 具体查看该方法所附带的说明.
        6. 忽略并不再接受来自对方的请求: `await event.ignoreAndBlock()`, 具体查看该方法所附带的说明.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `groupId: Union[int, NoneType]`
    :

    `groupName: str`
    :

    `message: str`
    :

    `nickname: str`
    :

    `requestId: int`
    :

    `supplicant: int`
    :

    `type: str`
    :

    ### Methods

    `accept(self, message: str = '') ‑> NoReturn`
    :   同意对方加入群组.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `ignore(self, message: str = '') ‑> NoReturn`
    :   忽略对方加入群组的请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `ignoreAndBlock(self, message: str = '') ‑> NoReturn`
    :   忽略对方加入群组的请求, 并不再接受来自对方加入群组的请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `reject(self, message: str = '') ‑> NoReturn`
    :   拒绝对方加入群组.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `rejectAndBlock(self, message: str = '') ‑> NoReturn`
    :   拒绝对方加入群组的请求, 并不再接受来自对方加入群组的请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

`MemberLeaveEventKick(**data: Any)`
:   该事件发生时, 有一群组成员被管理员/群主从群组中删除, 当 `operator` 为 `None` 时, 执行者为应用实例所辖账号.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 指定的群组
        Member (annotation):
          - `"target"` (default, const, str): 被从群组删除的成员
          - `"operator"` (default, const, str, return:optional): 执行了该操作的管理员/群主, 也可能是应用实例所辖账号.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `member: graia.application.group.Member`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `type: str`
    :

`MemberLeaveEventQuit(**data: Any)`
:   该事件发生时, 有一群组成员主动退出群组.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生本事件的群组, 通常的, 在本事件发生后本群组成员数量少于之前
        Member (annotation): 主动退出群组的成员
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `member: graia.application.group.Member`
    :

    `type: str`
    :

`MemberMuteEvent(**data: Any)`
:   该事件发生时, 有一群组成员被管理员/群组禁言, 当 `operator` 为 `None` 时为应用实例所辖账号操作.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生该事件的群组
        Member (annotation):
          - `"target"` (default, const, str): 被禁言的成员
          - `"operator"` (default, const, str, return:optional): 该操作的执行者, 也可能是应用实例所辖账号.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `durationSeconds: int`
    :

    `member: graia.application.group.Member`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `type: str`
    :

`MemberPermissionChangeEvent(**data: Any)`
:   该事件发生时, 有一群组成员的权限被更改/调整, 执行者只可能是群组的群主.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生该事件的群组
        Member (annotation): 被调整权限的群组成员
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: str`
    :

    `member: graia.application.group.Member`
    :

    `origin: str`
    :

    `type: str`
    :

`MemberSpecialTitleChangeEvent(**data: Any)`
:   该事件发生时, 有一群组成员的群头衔被更改, 执行者只可能是群组的群主.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生该事件的群组
        Member (annotation): 被更改群头衔的群组成员
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `current: str`
    :

    `member: graia.application.group.Member`
    :

    `origin: str`
    :

    `type: str`
    :

`MemberUnmuteEvent(**data: Any)`
:   该事件发生时, 有一群组成员被管理员/群组解除禁言, 当 `operator` 为 `None` 时为应用实例所辖账号操作.
    
    ** 注意: 当监听该事件或该类事件时, 请优先考虑使用原始事件类作为类型注解, 以此获得事件类实例, 便于获取更多的信息! **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
        Group (annotation): 发生该事件的群组
        Member (annotation):
          - `"target"` (default, const, str): 被禁言的成员
          - `"operator"` (default, const, str, return:optional): 该操作的执行者, 可能是管理员或是群主, 也可能是应用实例所辖账号.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `member: graia.application.group.Member`
    :

    `operator: Union[graia.application.group.Member, NoneType]`
    :

    `type: str`
    :

`NewFriendRequestEvent(**data: Any)`
:   当该事件发生时, 有一用户向机器人提起好友请求.
    
    ** 注意: 当监听该事件时, 请使用原始事件类作为类型注解, 以此获得事件类实例, 并执行相关操作. **
    
    Allowed Extra Parameters(提供的额外注解支持):
        GraiaMiraiApplication (annotation): 发布事件的应用实例
    
    Addon Introduction:
        该事件的处理需要你获取原始事件实例.
        1. 读取该事件的基础信息:
        ``` python
        event.supplicant: int # 发起加好友请求的用户的 ID
        event.sourceGroup: Optional[int] # 对方可能是从某个群发起对账号的请求的, mirai 可以解析对方从哪个群发起的请求.
        event.nickname: str # 对方的昵称
        event.message: str # 对方发起请求时填写的描述
        ```
    
        2. 同意请求: `await event.accept()`, 具体查看该方法所附带的说明.
        3. 拒绝请求: `await event.reject()`, 具体查看该方法所附带的说明.
        4. 拒绝并不再接受来自对方的请求: `await event.rejectAndBlock()`, 具体查看该方法所附带的说明.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `message: str`
    :

    `nickname: str`
    :

    `requestId: int`
    :

    `sourceGroup: Union[int, NoneType]`
    :

    `supplicant: int`
    :

    `type: str`
    :

    ### Methods

    `accept(self, message: str = '') ‑> NoReturn`
    :   同意对方的加好友请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `reject(self, message: str = '') ‑> NoReturn`
    :   拒绝对方的加好友请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.

    `rejectAndBlock(self, message: str = '') ‑> NoReturn`
    :   拒绝对方的加好友请求, 并不再接受来自对方的加好友请求.
        
        Args:
            message (str, optional): 附带给对方的消息. 默认为 "".
        
        Raises:
            LookupError: 尝试上下文外处理事件.
            InvaildSession: 应用实例没准备好!
        
        Returns:
            NoReturn: 没有返回.