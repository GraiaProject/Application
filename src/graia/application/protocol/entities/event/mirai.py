from typing import Optional

from pydantic import Field
from graia.application.protocol.entities.targets.group import Group, Member, MemberPerm
from . import MiraiEvent
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from datetime import datetime

class EmptyDispatcher(BaseDispatcher):
    @staticmethod
    def catch(interface):
        pass

class BotOnlineEvent(MiraiEvent):
    type = "BotOnlineEvent"
    qq: int

    Dispatcher = EmptyDispatcher

class BotOfflineEventActive(MiraiEvent):
    type = "BotOfflineEventActive"
    qq: int

    Dispatcher = EmptyDispatcher

class BotOfflineEventForce(MiraiEvent):
    type = "BotOfflineEventForce"
    qq: int

    Dispatcher = EmptyDispatcher

class BotOfflineEventDropped(MiraiEvent):
    type = "BotOfflineEventDropped"
    qq: int

    Dispatcher = EmptyDispatcher

class BotReloginEvent(MiraiEvent):
    type = "BotReloginEvent"
    qq: int

    Dispatcher = EmptyDispatcher

class BotGroupPermissionChangeEvent(MiraiEvent):
    type = "BotGroupPermissionChangeEvent"
    origin: MemberPerm
    current: MemberPerm
    group: Group

    Dispatcher = EmptyDispatcher

class BotMuteEvent(MiraiEvent):
    type = "BotMuteEvent"
    durationSeconds: int
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.operator

class BotUnmuteEvent(MiraiEvent):
    type = "BotUnmuteEvent"
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.operator

class BotJoinGroupEvent(MiraiEvent):
    type = "BotJoinGroupEvent"
    group: Group

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group

class GroupRecallEvent(MiraiEvent):
    type = "GroupRecallEvent"
    authorId: int
    messageId: int
    time: datetime
    group: Group
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group

class FriendRecallEvent(MiraiEvent):
    type = "FriendRecallEvent"
    authorId: int
    messageId: int
    time: int
    operator: int

class GroupNameChangeEvent(MiraiEvent):
    type = "GroupNameChangeEvent"
    origin: str
    current: str
    group: Group
    isByBot: bool

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group

class GroupEntranceAnnouncementChangeEvent(MiraiEvent):
    type = "GroupEntranceAnnouncementChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is Member:
                return interface.event.operator

class GroupMuteAllEvent(MiraiEvent):
    type = "GroupMuteAllEvent"
    origin: bool
    current: bool
    group: Group
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is Member:
                return interface.event.operator

class GroupAllowAnonymousChatEvent(MiraiEvent):
    type = "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is Member:
                return interface.event.operator

class GroupAllowConfessTalkEvent(MiraiEvent):
    type = "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group
    isByBot: bool

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is Member:
                return interface.event.operator

class GroupAllowMemberInviteEvent(MiraiEvent):
    type = "GroupAllowMemberInviteEvent"
    origin: bool
    current: bool
    group: Group
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.group
            elif interface.annotation is Member:
                return interface.event.operator

class MemberJoinEvent(MiraiEvent):
    type = "MemberJoinEvent"
    member: Member

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member

class MemberLeaveEventKick(MiraiEvent):
    type = "MemberLeaveEventKick"
    member: Member
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                if interface.default == "target":
                    return interface.event.member
                elif interface.default == "operator":
                    return interface.event.operator

class MemberLeaveEventQuit(MiraiEvent):
    type = "MemberLeaveEventQuit"
    member: Member

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member

class MemberCardChangeEvent(MiraiEvent):
    type = "MemberCardChangeEvent"
    origin: str
    current: str
    member: Member
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                if interface.default == "target":
                    return interface.event.member
                elif interface.default == "operator":
                    return interface.event.operator

class MemberSpecialTitleChangeEvent(MiraiEvent):
    type = "MemberSpecialTitleChangeEvent"
    origin: str
    current: str
    member: Member

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member

class MemberPermissionChangeEvent(MiraiEvent):
    type = "MemberPermissionChangeEvent"
    origin: str
    current: str
    member: Member

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                return interface.event.member

class MemberMuteEvent(MiraiEvent):
    type = "MemberMuteEvent"
    durationSeconds: int
    member: Member
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                if interface.default == "target":
                    return interface.event.member
                elif interface.default == "operator":
                    return interface.event.operator

class MemberUnmuteEvent(MiraiEvent):
    type = "MemberUnmuteEvent"
    member: Member
    operator: Optional[Member]

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Member:
                if interface.default == "target":
                    return interface.event.member
                elif interface.default == "operator":
                    return interface.event.operator

class NewFriendRequestEvent(MiraiEvent):
    type = "NewFriendRequestEvent"
    requestId: int = Field(..., alias="eventId")
    supplicant: int = Field(..., alias="fromId") # 即请求方 QQ
    sourceGroup: Optional[int] = Field(..., alias="groupId")
    nickname: str = Field(..., alias="nick")
    message: str

class MemberJoinRequestEvent(MiraiEvent):
    type = "MemberJoinRequestEvent"
    requestId: int = Field(..., alias="eventId")
    supplicant: int = Field(..., alias="fromId") # 即请求方 QQ
    groupId: Optional[int] = Field(..., alias="groupId")
    groupName: str = Field(..., alias="groupName")
    nickname: str = Field(..., alias="nick")
    message: str

class BotInvitedJoinGroupRequestEvent(MiraiEvent):
    type = "BotInvitedJoinGroupRequestEvent"
    requestId: int = Field(..., alias="eventId")
    supplicant: int = Field(..., alias="fromId") # 即请求方 QQ
    groupId: Optional[int] = Field(..., alias="groupId")
    groupName: str = Field(..., alias="groupName")
    nickname: str = Field(..., alias="nick")
    message: str