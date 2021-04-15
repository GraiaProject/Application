Module graia.application.event
==============================

Sub-modules
-----------
* graia.application.event.dispatcher
* graia.application.event.lifecycle
* graia.application.event.messages
* graia.application.event.mirai
* graia.application.event.network

Classes
-------

`ApplicationDispatcher()`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

`EmptyDispatcher()`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

`MiraiEvent(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.event.messages.Forward
    * graia.application.event.messages.FriendMessage
    * graia.application.event.messages.GroupMessage
    * graia.application.event.messages.TempMessage
    * graia.application.event.mirai.BotGroupPermissionChangeEvent
    * graia.application.event.mirai.BotInvitedJoinGroupRequestEvent
    * graia.application.event.mirai.BotJoinGroupEvent
    * graia.application.event.mirai.BotLeaveEventActive
    * graia.application.event.mirai.BotLeaveEventKick
    * graia.application.event.mirai.BotMuteEvent
    * graia.application.event.mirai.BotOfflineEventActive
    * graia.application.event.mirai.BotOfflineEventDropped
    * graia.application.event.mirai.BotOfflineEventForce
    * graia.application.event.mirai.BotOnlineEvent
    * graia.application.event.mirai.BotReloginEvent
    * graia.application.event.mirai.BotUnmuteEvent
    * graia.application.event.mirai.FriendRecallEvent
    * graia.application.event.mirai.GroupAllowAnonymousChatEvent
    * graia.application.event.mirai.GroupAllowConfessTalkEvent
    * graia.application.event.mirai.GroupAllowMemberInviteEvent
    * graia.application.event.mirai.GroupEntranceAnnouncementChangeEvent
    * graia.application.event.mirai.GroupMuteAllEvent
    * graia.application.event.mirai.GroupNameChangeEvent
    * graia.application.event.mirai.GroupRecallEvent
    * graia.application.event.mirai.MemberCardChangeEvent
    * graia.application.event.mirai.MemberJoinEvent
    * graia.application.event.mirai.MemberJoinRequestEvent
    * graia.application.event.mirai.MemberLeaveEventKick
    * graia.application.event.mirai.MemberLeaveEventQuit
    * graia.application.event.mirai.MemberMuteEvent
    * graia.application.event.mirai.MemberPermissionChangeEvent
    * graia.application.event.mirai.MemberSpecialTitleChangeEvent
    * graia.application.event.mirai.MemberUnmuteEvent
    * graia.application.event.mirai.NewFriendRequestEvent

    ### Class variables

    `Config`
    :

    `Dispatcher`
    :

    `type: str`
    :

    ### Static methods

    `type_limit(v)`
    :