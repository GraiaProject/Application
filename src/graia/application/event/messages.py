from pydantic import validator

from graia.application.event.dispatcher import MessageChainCatcher
from graia.application.message.chain import MessageChain
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.application.group import Member, Group
from graia.application.friend import Friend
from graia.application.message.elements.internal import Source
from . import ApplicationDispatcher, MiraiEvent


class SourceElementDispatcher(BaseDispatcher):
    @staticmethod
    def catch(interface: DispatcherInterface):
        if interface.annotation is Source:
            return interface.event.messageChain.getFirst(Source)


class FriendMessage(MiraiEvent):
    type: str = "FriendMessage"
    messageChain: MessageChain
    sender: Friend

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher, SourceElementDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Friend:
                return interface.event.sender


class GroupMessage(MiraiEvent):
    type: str = "GroupMessage"
    messageChain: MessageChain
    sender: Member

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher, SourceElementDispatcher]

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
    def parse_obj(cls, obj):
        return super().parse_obj(obj)

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher, SourceElementDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender
