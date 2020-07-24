import asyncio
from typing import List, NoReturn, Optional, Tuple, Union

from aiohttp import ClientSession, FormData
from graia.application.context import enter_message_send_context
from graia.application.protocol.entities.event.messages import (FriendMessage,
                                                                GroupMessage,
                                                                TempMessage)
from graia.application.protocol.entities.message import BotMessage
from graia.application.protocol.entities.message.chain import MessageChain
from graia.application.protocol.entities.message.elements import external
from graia.application.protocol.entities.message.elements.internal import (
    Image, Source)
from graia.application.protocol.entities.session import Session
from graia.application.protocol.exceptions import (InvaildArgument,
                                                   InvaildSession)
from graia.application.protocol.utilles import (AppMiddlewareAsDispatcher,
                                                SinceVersion,
                                                raise_for_return_code,
                                                requireAuthenticated)
from graia.broadcast import Broadcast
from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.utilles import run_always_await
from yarl import URL

from .protocol import UploadMethods
from .protocol.entities.targets.friend import Friend
from .protocol.entities.targets.group import (Group, GroupConfig, Member,
                                              MemberInfo)


class GraiaMiraiApplication:
    broadcast: Broadcast
    session: ClientSession
    connect_info: Session

    def __init__(self, *,
        broadcast: Broadcast,
        connect_info: Session,
        session: Optional[ClientSession] = None
    ):
        self.broadcast = broadcast
        self.connect_info = connect_info
        self.session = session or ClientSession(loop=broadcast.loop)
        self.broadcast.getDefaultNamespace().injected_dispatchers.append(
            AppMiddlewareAsDispatcher(self)
        )

    def url_gen(self, path) -> str:
        return str(URL(str(self.connect_info.host)).parent / path)
    
    @SinceVersion(1,6,2)
    async def getVersion(self, auto_set=True) -> Tuple:
        async with self.session.get(self.url_gen("about")) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            version = (int(i) for i in data['data']['version'][1:].split("."))
            if auto_set:
                self.connect_info.current_version = version
            return version

    async def authenticate(self) -> str:
        async with self.session.post(self.url_gen("auth"), json={
            "authKey": self.connect_info.authKey
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            self.connect_info.sessionKey = data['session']
            return data['session']

    async def activeSession(self) -> NoReturn:
        if not self.connect_info.sessionKey:
            raise InvaildSession("you should call 'authenticate' before this to get a sessionKey!")
        async with self.session.post(self.url_gen("verify"), json={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    async def signout(self) -> NoReturn:
        if not self.connect_info.sessionKey:
            raise InvaildSession("you should call 'authenticate' before this to get a sessionKey!")
        async with self.session.post(self.url_gen("release"), json={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def getGroup(self, group_id: int) -> Optional[Group]:
        data = await self.groupList()
        for i in data:
            if i.id == group_id:
                return i

    @requireAuthenticated
    async def groupList(self) -> List[Group]:
        async with self.session.get(
            str(URL(self.url_gen("groupList")).with_query({
                "sessionKey": self.connect_info.sessionKey
            }))
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Group.parse_obj(i) for i in data]

    @requireAuthenticated
    async def getMember(self, group: Union[Group, int], member_id: int) -> Member:
        data = await self.memberList(group)
        for i in data:
            if i.id == member_id:
                return i

    @requireAuthenticated
    async def memberList(self, group: Union[Group, int]) -> List[Member]:
        async with self.session.get(
            str(URL(self.url_gen("memberList")).with_query({
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group
            }))
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Member.parse_obj(i) for i in data]

    @requireAuthenticated
    async def friendList(self) -> List[Friend]:
        async with self.session.get(
            str(URL(self.url_gen("friendList")).with_query({
                "sessionKey": self.connect_info.sessionKey
            }))
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Friend.parse_obj(i) for i in data]

    @requireAuthenticated
    async def getFriend(self, friend_id: int) -> Friend:
        data = await self.friendList()
        for i in data:
            if i.id == friend_id:
                return i

    @requireAuthenticated
    async def uploadImage(self, image_bytes: bytes, method: UploadMethods) -> Image:
        data = FormData()
        data.add_field("sessionKey", self.connect_info.sessionKey)
        data.add_field("type", method.value)
        data.add_field("img", image_bytes)
        async with self.session.post(self.url_gen("uploadImage"), data=data) as response:
            response.raise_for_status()
            resp_json = await response.json()
            raise_for_return_code(resp_json)
            return Image.fromExternal(external.Image.parse_obj(resp_json))

    @requireAuthenticated
    async def sendFriendMessage(self, target: Union[Friend, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        with enter_message_send_context(UploadMethods.Friend):
            async with self.session.post(self.url_gen("sendFriendMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "target": target.id if isinstance(target, Friend) else target,
                "messageChain": await message.build(),
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)
                return BotMessage(messageId=data['messageId'])

    @requireAuthenticated
    async def sendGroupMessage(self, group: Union[Group, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        with enter_message_send_context(UploadMethods.Group):
            async with self.session.post(self.url_gen("sendGroupMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "messageChain": (await message.build()).dict()['__root__'],
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)
                return BotMessage(messageId=data['messageId'])
    
    @requireAuthenticated
    async def sendTempMessage(self,
        group: Union[Group, int],
        target: Union[Member, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        with enter_message_send_context(UploadMethods.Temp):
            async with self.session.post(self.url_gen("sendTempMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "group": group.id if isinstance(group, Group) else group,
                "qq": target.id if isinstance(target, Friend) else target,
                "messageChain": await message.build(),
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)
                return BotMessage(messageId=data['messageId'])

    @requireAuthenticated
    async def revokeMessage(self,
        target: Union[Source, BotMessage, int]
    ) -> NoReturn:
        async with self.session.post(self.url_gen("recall"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": target.id if isinstance(target, (Source, BotMessage)) else id
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
    
    @requireAuthenticated
    async def fetchMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("fetchMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for i in data['data']:
                if i['type'] == "GroupMessage":
                    result.append(GroupMessage.parse_obj(i))
                elif i['type'] == "FriendMessage":
                    result.append(FriendMessage.parse_obj(i))
                elif i['type'] == "TempMessage":
                    result.append(TempMessage.parse_obj(i))
            return result
    
    @requireAuthenticated
    async def fetchLatestMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("fetchLatestMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for i in data['data']:
                if i['type'] == "GroupMessage":
                    result.append(GroupMessage.parse_obj(i))
                elif i['type'] == "FriendMessage":
                    result.append(FriendMessage.parse_obj(i))
                elif i['type'] == "TempMessage":
                    result.append(TempMessage.parse_obj(i))
            return result

    @requireAuthenticated
    async def peekMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("peekMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for i in data['data']:
                if i['type'] == "GroupMessage":
                    result.append(GroupMessage.parse_obj(i))
                elif i['type'] == "FriendMessage":
                    result.append(FriendMessage.parse_obj(i))
                elif i['type'] == "TempMessage":
                    result.append(TempMessage.parse_obj(i))
            return result
    
    @requireAuthenticated
    async def peekLatestMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("peekLatestMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for i in data['data']:
                if i['type'] == "GroupMessage":
                    result.append(GroupMessage.parse_obj(i))
                elif i['type'] == "FriendMessage":
                    result.append(FriendMessage.parse_obj(i))
                elif i['type'] == "TempMessage":
                    result.append(TempMessage.parse_obj(i))
            return result

    @requireAuthenticated
    async def messageFromId(self, source: Union[Source, int]) -> Union[GroupMessage, TempMessage, FriendMessage]:
        async with self.session.get(str(URL(self.url_gen("messageFromId")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "id": source.id if isinstance(source, Source) else source
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            if data['data']['type'] == "GroupMessage":
                return GroupMessage.parse_obj(data['data'])
            elif data['data']['type'] == "FriendMessage":
                return FriendMessage.parse_obj(data['data'])
            elif data['data']['type'] == "TempMessage":
                return TempMessage.parse_obj(data['data'])

    @requireAuthenticated
    async def countMessage(self) -> int:
        async with self.session.get(str(URL(self.url_gen("countMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return data['data']

    @requireAuthenticated
    async def muteAll(self, group: Union[Group, int]) -> NoReturn:
        async with self.session.post(self.url_gen("muteAll"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def unmuteAll(self, group: Union[Group, int]) -> NoReturn:
        async with self.session.post(self.url_gen("unmuteAll"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def mute(self, group: Union[Group, int], member: Union[Member, int], time: int) -> NoReturn:
        time = max(0, min(time, 30*24*60*60))
        async with self.session.post(self.url_gen("mute"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member,
            "time": time
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
    
    @requireAuthenticated
    async def unmute(self, group: Union[Group, int], member: Union[Member, int]) -> NoReturn:
        async with self.session.post(self.url_gen("unmute"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
    
    @requireAuthenticated
    async def kick(self, group: Union[Group, int], member: Union[Member, int], message: Optional[str] = None) -> NoReturn:
        async with self.session.post(self.url_gen("kick"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member,
            **({
                "msg": message
            } if message else {})
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def quit(self, group: Union[Group, int]) -> NoReturn:
        async with self.session.post(self.url_gen("quit"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def getGroupConfig(self, group: Union[Group, int]) -> GroupConfig:
        async with self.session.get(str(URL(self.url_gen("groupConfig")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return GroupConfig.parse_obj(data)

    @requireAuthenticated
    async def modifyGroupConfig(self, group: Union[Group, int], config: GroupConfig) -> NoReturn:
        async with self.session.post(self.url_gen("groupConfig"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "config": config.json(exclude_none=True, exclude_unset=True, by_alias=True)
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    async def getMemberInfo(self, member: Union[Member, int], group: Optional[Union[Group, int]] = None) -> MemberInfo:
        if not group and not isinstance(member, Member):
            raise TypeError("you should give a Member instance if you cannot give a Group instance to me.")
        if isinstance(member, Member) and not group:
            group: Group = member.group
        async with self.session.get(str(URL(self.url_gen("memberInfo")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return MemberInfo.parse_obj(data)

    @requireAuthenticated
    async def modifyMemberInfo(self, member: Union[Member, int], info: MemberInfo, group: Optional[Union[Group, int]] = None) -> NoReturn:
        if not group and not isinstance(member, Member):
            raise TypeError("you should give a Member instance if you cannot give a Group instance to me.")
        if isinstance(member, Member) and not group:
            group: Group = member.group
        async with self.session.post(self.url_gen("memberInfo"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member,
            "info": info.json(exclude_none=True, exclude_unset=True, by_alias=True)
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @staticmethod
    async def auto_parse_by_type(original_dict: dict) -> BaseEvent:
        if not original_dict.get("type") and not isinstance(original_dict.get("type"), str):
            raise InvaildArgument("you need to provide a 'type' field for automatic parsing")
        event_type = Broadcast.findEvent(original_dict.get("type"))
        if not event_type:
            raise ValueError("we cannot find a such event: {}".format(original_dict.get("type")))
        return await run_always_await(event_type.parse_obj({
            k: v for k, v in original_dict.items() if k != "type"
        }))

    @requireAuthenticated
    async def ws_all_poster(self):
        async with self.session.ws_connect(str(URL(self.url_gen("all")).with_query({
            "sessionKey": self.connect_info.sessionKey
        }))) as connection:
            while True:
                try:
                    received_data = await connection.receive_json()
                    #print("d", received_data)
                except TypeError:
                    continue
                if received_data:
                    try:
                        event = await self.auto_parse_by_type(received_data)
                    except ValueError:
                        # TODO: logger
                        raise
                        print("received a unknown event:", received_data.get("type"), received_data)
                        continue
                    self.broadcast.postEvent(event)
    
    def launch_with(self, event_poster=ws_all_poster):
        from graia.application.protocol.entities.event.lifecycle import (
            ApplicationLaunched, ApplicationShutdowned)
        loop = self.broadcast.loop
        loop.run_until_complete(self.authenticate())
        loop.run_until_complete(self.activeSession())
        loop.run_until_complete(self.broadcast.layered_scheduler(
            listener_generator=self.broadcast.default_listener_generator(ApplicationLaunched),
            event=ApplicationLaunched(self)
        ))
        try:
            loop.run_until_complete(event_poster(self))
        finally:
            loop.run_until_complete(self.broadcast.layered_scheduler(
                listener_generator=self.broadcast.default_listener_generator(ApplicationLaunched),
                event=ApplicationShutdowned(self)
            ))
            loop.run_until_complete(self.signout())
            loop.run_until_complete(self.session.close())
