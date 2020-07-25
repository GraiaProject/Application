from inspect import iscoroutine

from pydantic import validator

from graia.application.protocol.entities.event.dispatcher import MessageChainCatcher
from graia.application.protocol.entities.message.chain import MessageChain
from graia.application.protocol.entities.targets import friend
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.application.protocol.entities.targets.group import Member, Group
from graia.application.protocol.entities.targets.friend import Friend
from . import ApplicationDispatcher, MiraiEvent

class FriendMessage(MiraiEvent):
    type: str = "FriendMessage"
    messageChain: MessageChain
    sender: Friend

    @classmethod
    async def parse_obj(cls, obj):
        mec = obj.get("messageChain")
        if iscoroutine(mec):
            obj['messageChain'] = await mec
        return super().parse_obj(obj)
    
    @validator("messageChain")
    def _(cls, v):
        return 

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Friend:
                return interface.event.sender

class GroupMessage(MiraiEvent):
    type: str = "GroupMessage"
    messageChain: MessageChain
    sender: Member

    @classmethod
    def parse_obj(cls, obj):
        return super().parse_obj(obj)

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender

class TempMessage(MiraiEvent):
    type: str = "TempMessage"
    messageChain: MessageChain
    sender: Member

    @classmethod
    async def parse_obj(cls, obj):
        mec = obj.get("messageChain")
        if iscoroutine(mec):
            obj['messageChain'] = await mec
        return super().parse_obj(obj)

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender