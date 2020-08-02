import asyncio
import atexit
from typing import List, NoReturn, Optional, Tuple, Union
from .logger import AbstractLogger, LoggingLogger
from .entities import MiraiConfig

import graia.application.event.mirai  # for init events
from aiohttp import ClientSession, FormData
from graia.broadcast import Broadcast
from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.utilles import printer, run_always_await
from yarl import URL
from functools import partial

from .context import enter_message_send_context
from .entities import UploadMethods
from .event.messages import (FriendMessage, GroupMessage,
                                               TempMessage)
from .message import BotMessage
from .message.chain import MessageChain
from .message.elements import external
from .message.elements.internal import Image, Source
from .session import Session
from .friend import Friend
from .group import (Group, GroupConfig, Member, MemberInfo)
from .exceptions import InvaildArgument, InvaildSession
from .utilles import (AppMiddlewareAsDispatcher, SinceVersion,
                               raise_for_return_code, requireAuthenticated)


class GraiaMiraiApplication:
    broadcast: Broadcast
    session: ClientSession
    connect_info: Session
    logger: AbstractLogger

    def __init__(self, *,
        broadcast: Broadcast,
        connect_info: Session,
        session: Optional[ClientSession] = None,
        logger: Optional[AbstractLogger] = None
    ):
        self.broadcast = broadcast
        self.connect_info = connect_info
        self.session = session or ClientSession(loop=broadcast.loop)
        self.logger = logger or LoggingLogger()
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
    async def uploadImage(self, image_bytes: bytes, method: UploadMethods, return_external: bool = False) -> Image:
        data = FormData()
        data.add_field("sessionKey", self.connect_info.sessionKey)
        data.add_field("type", method.value)
        data.add_field("img", image_bytes)
        async with self.session.post(self.url_gen("uploadImage"), data=data) as response:
            response.raise_for_status()
            resp_json = await response.json()
            raise_for_return_code(resp_json)
            external_component = external.Image.parse_obj(resp_json)
            if return_external:
                return external_component
            else:
                return Image.fromExternal(external_component)
            

    @requireAuthenticated
    async def sendFriendMessage(self, target: Union[Friend, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        with enter_message_send_context(UploadMethods.Friend):
            async with self.session.post(self.url_gen("sendFriendMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "target": target.id if isinstance(target, Friend) else target,
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
                "qq": target.id if isinstance(target, Member) else target,
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

    @requireAuthenticated
    async def getConfig(self) -> MiraiConfig:
        async with self.session.get(str(URL(self.url_gen("config")).with_query({
            "sessionKey": self.connect_info.sessionKey
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return MiraiConfig.parse_obj(data)

    @requireAuthenticated
    async def modifyConfig(self, *, cacheSize=None, enableWebsocket=None) -> NoReturn:
        if any([cacheSize is not None, enableWebsocket is not None]):
            async with self.session.post(self.url_gen("config"), json={
                "sessionKey": self.connect_info.sessionKey,
                **({"cacheSize": cacheSize} if cacheSize is not None else {}),
                **({"enableWebsocket": enableWebsocket} if enableWebsocket is not None else {}),
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
                    except ValueError as e:
                        self.logger.error("".join(["received a unknown event: ", received_data.get("type"), str(received_data)]))
                        continue
                    self.broadcast.postEvent(event)
    
    @requireAuthenticated
    async def http_fetchmessage_poster(self, delay=0.5, fetch_num=10):
        while True:
            await asyncio.sleep(delay)
            while True:
                data = await self.fetchMessage(fetch_num)
                for i in data:
                    self.broadcast.postEvent(i)
                if len(data) != fetch_num:
                    break

    async def launch(self):
        from .event.lifecycle import ApplicationLaunched
        self.logger.info("launching app...")
        await self.authenticate()
        await self.activeSession()
        await self.broadcast.layered_scheduler(
            listener_generator=self.broadcast.default_listener_generator(ApplicationLaunched),
            event=ApplicationLaunched(self)
        )

        # 自动变化fetch方式
        fetch_method = self.http_fetchmessage_poster if not self.connect_info.websocket else self.ws_all_poster
        config: MiraiConfig = await self.getConfig()
        if not self.connect_info.websocket: # 不启用 websocket
            self.logger.info("using websocket to receive event")
            if config.enableWebsocket: # 配置中已经启用
                await self.modifyConfig(enableWebsocket=False)
        else: # 启用ws
            self.logger.info("using pure websocket to receive event")
            if not config.enableWebsocket: # 配置中没启用
                await self.modifyConfig(enableWebsocket=True)

        self.logger.info("event reveiver running...")
        return fetch_method()

    async def shutdown(self):
        from .event.lifecycle import ApplicationShutdowned
        self.logger.info("application shutdowning...")
        await self.broadcast.layered_scheduler(
            listener_generator=self.broadcast.default_listener_generator(ApplicationShutdowned),
            event=ApplicationShutdowned(self)
        )
        await self.signout()
        await self.session.close()
        self.logger.info("goodbye :)")

    def launch_blocking(self):
        loop = asyncio.get_event_loop()
        try:
            fetch_method = loop.run_until_complete(self.launch())
            loop.run_until_complete(fetch_method)
        finally:
            loop.run_until_complete(self.shutdown())

    def subscribe_atexit(self, loop=None):
        loop = loop or self.broadcast.loop
        atexit.register(partial(loop.run_until_complete, self.shutdown()))

    def create_background_task(self, loop=None):
        loop = loop or self.broadcast.loop
        return loop.create_task(loop.run_until_complete(self.launch()))