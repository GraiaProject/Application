from inspect import iscoroutine
from pydantic import BaseModel, validator
from graia.broadcast import BaseEvent
from pydantic.main import ModelMetaclass

from graia.application.protocol.exceptions import (
    InvalidEventTypeDefinition)
from graia.application.protocol.entities.event.dispatcher import MessageChainCatcher
from graia.application.protocol.entities.message.chain import MessageChain
from graia.application.protocol.entities.targets import friend
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.application.protocol.entities.targets.group import Member, Group
from graia.application.protocol.entities.targets.friend import Friend


class MiraiEvent(BaseEvent, BaseModel):
    __base_event__ = True
    type: str

    @validator("type")
    def type_limit(cls, v):
        if cls.type != v:
            raise InvalidEventTypeDefinition("{0}'s type must be '{1}', not '{2}'".format(cls.__name__, cls.type, v))
        return v

    class Config:
        extra = "forbid"

    class Dispatcher:
        pass

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

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher]

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
        print("?", obj)
        return super().parse_obj(obj)

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher]

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
        mixin = [MessageChainCatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender