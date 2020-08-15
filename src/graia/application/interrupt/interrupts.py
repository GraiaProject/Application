from typing import Any, Callable, Optional, Type, TypeVar, Union

from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.utilles import run_always_await

from graia.application.group import Group, Member
from graia.application.friend import Friend
from . import Interrupt
from graia.application.event.messages import FriendMessage, GroupMessage, TempMessage
from graia.application.message import BotMessage
from graia.application.message.elements.internal import Quote, Source

class GroupMessageInterrupt(Interrupt):
    direct = GroupMessage
    special_group: Optional[Union[Group, int]] = None
    special_member: Optional[Union[Member, int]] = None
    quote_access: Optional[Union[BotMessage, Source]] = None
    custom_judgement: Optional[Callable[[GroupMessage], bool]] = None

    def __init__(self,
        special_group: Optional[Union[Group, int]] = None,
        special_member: Optional[Union[Member, int]] = None,
        quote_access: Optional[Union[BotMessage, Source]] = None,
        custom_judgement: Optional[Callable[[GroupMessage], bool]] = None,
        block_propagation: bool = False
    ) -> None:
        self.special_group = special_group
        self.special_member = special_member
        self.quote_access = quote_access
        self.custom_judgement = custom_judgement
        self._block_propagation = block_propagation

    def set_custom_judgement(self, callable_func):
        self.custom_judgement = callable_func
        return callable_func

    def trigger(self, event: GroupMessage) -> Union[None, GroupMessage]:
        if self.special_group:
            if event.sender.group.id != (self.special_group.id if isinstance(self.special_group, Group) else self.special_group):
                return None
        if self.special_member:
            if event.sender.id != (self.special_member.id if isinstance(self.special_member, Member) else self.special_member):
                return None
        if self.quote_access:
            quotes = event.messageChain.get(Quote)
            if not quotes:
                return
            quote: Quote = quotes[0]
            if isinstance(self.quote_access, BotMessage):
                if quote.id != self.quote_access.messageId:
                    return None
            elif isinstance(self.quote_access, Source):
                if quote.id != self.quote_access.id:
                    return None
        if self.custom_judgement:
            if not self.custom_judgement(event):
                return None
        return event

class FriendMessageInterrupt(Interrupt):
    direct = FriendMessage

    special_friend: Optional[Union[Friend, int]] = None
    quote_access: Optional[Union[BotMessage, Source]] = None
    custom_judgement: Optional[Callable[[FriendMessage], bool]] = None

    def __init__(self,
        special_friend: Optional[Union[Friend, int]] = None,
        quote_access: Optional[Union[BotMessage, Source]] = None,
        custom_judgement: Optional[Callable[[FriendMessage], bool]] = None,
        block_propagation: bool = False
    ) -> None:
        self.special_friend = special_friend
        self.quote_access = quote_access
        self.custom_judgement = custom_judgement
        self._block_propagation = block_propagation

    def set_custom_judgement(self, callable_func):
        self.custom_judgement = callable_func
        return callable_func

    def trigger(self, event: FriendMessage) -> Union[None, FriendMessage]:
        if self.special_friend:
            if event.sender.id != (self.special_friend.id if isinstance(self.special_friend, Friend) else self.special_friend):
                return
        if self.quote_access:
            quotes = event.messageChain.get(Quote)
            if not quotes:
                return
            quote: Quote = quotes[0]
            if isinstance(self.quote_access, BotMessage):
                if quote.id != self.quote_access.messageId:
                    return None
            elif isinstance(self.quote_access, Source):
                if quote.id != self.quote_access.id:
                    return None
        if self.custom_judgement:
            if not self.custom_judgement(event):
                return None
        return event

class TempMessageInterrupt(Interrupt):
    direct = TempMessage
    special_group: Optional[Union[Group, int]] = None
    special_member: Optional[Union[Member, int]] = None
    quote_access: Optional[Union[BotMessage, Source]] = None
    custom_judgement: Optional[Callable[[TempMessage], bool]] = None

    def __init__(self,
        special_group: Optional[Union[Group, int]] = None,
        special_member: Optional[Union[Member, int]] = None,
        quote_access: Optional[Union[BotMessage, Source]] = None,
        custom_judgement: Optional[Callable[[TempMessage], bool]] = None,
        block_propagation: bool = False
    ) -> None:
        self.special_group = special_group
        self.special_member = special_member
        self.quote_access = quote_access
        self.custom_judgement = custom_judgement
        self._block_propagation = block_propagation

    def set_custom_judgement(self, callable_func):
        self.custom_judgement = callable_func
        return callable_func

    def trigger(self, event: TempMessage) -> Union[None, TempMessage]:
        if self.special_group:
            if event.sender.group.id != (self.special_group.id if isinstance(self.special_group, Group) else self.special_group):
                return None
        if self.special_member:
            if event.sender.id != (self.special_member.id if isinstance(self.special_member, Member) else self.special_member):
                return None
        if self.quote_access:
            quotes = event.messageChain.get(Quote)
            if not quotes:
                return
            quote: Quote = quotes[0]
            if isinstance(self.quote_access, BotMessage):
                if quote.id != self.quote_access.messageId:
                    return None
            elif isinstance(self.quote_access, Source):
                if quote.id != self.quote_access.id:
                    return None
        if self.custom_judgement:
            if not self.custom_judgement(event):
                return None
        return event

T = TypeVar("T", BaseEvent, Any)
A = TypeVar("A")

class CustomEventInterrupt(Interrupt):
    def __init__(self,
        event: Type[T],
        checker: Callable[[T], bool],
        transfer: Callable[[T], A],
        block_propagation: bool = False
    ) -> None:
        self.direct = event
        self.checker = checker
        self.transfer = transfer
        self._block_propagation = block_propagation
    
    async def trigger(self, event: T) -> Union[None, A]:
        if await run_always_await(self.checker(event)):
            return await run_always_await(self.transfer(event))