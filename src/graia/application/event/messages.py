from typing import List
from datetime import datetime
from pydantic import validator, Field
from pydantic.main import BaseModel

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
    async def catch(interface: DispatcherInterface):
        if interface.annotation is Source:
            return interface.event.messageChain.getFirst(Source)


class FriendMessage(MiraiEvent):
    type: str = "FriendMessage"
    messageChain: MessageChain
    sender: Friend

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher, SourceElementDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Friend:
                return interface.event.sender


class GroupMessage(MiraiEvent):
    type: str = "GroupMessage"
    messageChain: MessageChain
    sender: Member

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher, SourceElementDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
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
        async def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender


class ForwardContentMessage(BaseModel):
    senderId: int
    senderName: str

    messageChain: MessageChain

    time: datetime


class Forward(MiraiEvent):
    type: str = "Forward"

    "表示该条转发消息的标题, 通常为 `群聊的聊天记录`"
    title: str

    "显示在消息列表中的预览文本, 调用 asDisplay 方法返回该值"
    brief: str

    "似乎没有什么用, 这个东西找不到在哪里显示"
    source: str

    "描述, 通常都像: `查看 x 条转发消息` 这样"
    summary: str

    content: List[ForwardContentMessage] = Field(..., alias="nodeList")

    def asDisplay(self):
        return self.brief

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher]

        @staticmethod
        async def catch(interface: DispatcherInterface):
            pass
