import asyncio
import atexit
from functools import partial
from typing import List, NoReturn, Optional, Tuple, Union

import graia.application.event.lifecycle
import graia.application.event.mirai  # for init events
from aiohttp import ClientSession, FormData
from graia.application.event import MiraiEvent
from graia.broadcast import Broadcast
from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.entities.inject_rule import SpecialEventType
from graia.broadcast.utilles import printer, run_always_await
from yarl import URL

from .context import enter_message_send_context
from .entities import MiraiConfig, UploadMethods
from .event.messages import FriendMessage, GroupMessage, TempMessage
from .exceptions import InvaildArgument, InvaildSession
from .friend import Friend
from .group import Group, GroupConfig, Member, MemberInfo
from .logger import AbstractLogger, LoggingLogger
from .message import BotMessage
from .message.chain import MessageChain
from .message.elements import external
from .message.elements.internal import Image, Source
from .session import Session
from .utilles import (AppMiddlewareAsDispatcher, SinceVersion,
                      raise_for_return_code, requireAuthenticated,
                      applicationContextManager)

class GraiaMiraiApplication:
    """本类的实例即 应用实例(Application), 是面向 `mirai-api-http` 接口的实际功能实现.
    你的应用大多都围绕着本类及本类的实例展开.  
    
    Attributes:
        broadcast (Broadcast): 被指定的, 外置的事件系统, 即 `Broadcast Control`,
            通常你不需要干涉该属性;
        session (ClientSession): 即 `aiohttp.ClientSession` 的实例, 用于与 `mirai-api-http` 通讯.
        connect_info (Session): 用于描述会话对象, 其中最重要的属性是 `sessionKey`, 用于存储当前的会话标识.
        logger (AbstractLogger): 日志系统实现类的实例, 默认以 `logging` 为日志驱动.
    """

    __slots__ = (
        "broadcast",
        "session",
        "connect_info",
        "logger",
        "debug"
    )

    broadcast: Broadcast
    session: ClientSession
    connect_info: Session
    logger: AbstractLogger
    debug: bool

    def __init__(self, *,
        broadcast: Broadcast,
        connect_info: Session,
        session: Optional[ClientSession] = None,
        logger: Optional[AbstractLogger] = None,
        debug: bool = False,
        enable_chat_log: bool = True
    ):
        self.broadcast = broadcast
        self.connect_info = connect_info
        self.session = session or ClientSession(loop=broadcast.loop)
        self.logger = logger or LoggingLogger(**({
            "debug": True
        } if debug else {}))
        self.debug = debug

        if enable_chat_log:
            self.broadcast.receiver("GroupMessage")(self.logger_group_message)
            self.broadcast.receiver("FriendMessage")(self.logger_friend_message)
            self.broadcast.receiver("TempMessage")(self.logger_temp_message)

        self.broadcast.addInjectionRule(
            SpecialEventType(MiraiEvent, AppMiddlewareAsDispatcher(self))
        )
    
    def logger_group_message(self, event: GroupMessage):
        self.logger.info("[BOT {bot_id}, GroupMessage] [{group_name}({group_id}, perm: {bot_permission})] {member_name}({member_id}, {member_permission}) -> {message_string}".format_map(dict(
            group_id=event.sender.group.id,
            group_name=event.sender.group.name,
            member_id=event.sender.id,
            member_name=event.sender.name,
            member_permission=event.sender.permission.name,
            bot_id=self.connect_info.account,
            bot_permission=event.sender.group.accountPerm.name,
            message_string=event.messageChain.asSerializationString(),
        )))
    
    def logger_friend_message(self, event: FriendMessage):
        self.logger.info("[BOT {bot_id}, FriendMessage] {friend_name}({friend_id}) -> {message_string}".format_map(dict(
            bot_id=self.connect_info.account,
            friend_name=event.sender.nickname,
            friend_id=event.sender.id,
            message_string=event.messageChain.asSerializationString()
        )))
    
    def logger_temp_message(self, event: TempMessage):
        self.logger.info("[BOT {bot_id}, TempMessage] [{group_name}({group_id}, perm: {bot_permission})] {member_name}({member_id}, {member_permission}) -> {message_string}".format_map(dict(
            group_id=event.sender.group.id,
            group_name=event.sender.group.name,
            member_id=event.sender.id,
            member_name=event.sender.name,
            member_permission=event.sender.permission.name,
            bot_id=self.connect_info.account,
            bot_permission=event.sender.group.accountPerm.name,
            message_string=event.messageChain.asSerializationString(),
        )))

    def url_gen(self, path) -> str:
        """从 connect_info 和 path 生成接口的地址.

        Args:
            path (str): 需求的接口地址

        Returns:
            str: 作为结果的地址
        """
        return str(URL(str(self.connect_info.host)).parent / path)
    
    @SinceVersion(1,6,2)
    @applicationContextManager
    async def getVersion(self, auto_set=True) -> Tuple:
        """从 `/about` 路由下获取当前使用的 `mirai-api-http` 版本, 注意, 该 API 并不是一开始就有的(1.6.2 版本才支持本接口).

        Args:
            auto_set (bool, optional): 是否自动将版本存入 connect_info 以判断接口是否有效. Defaults to True.

        Returns:
            Tuple: 以元组形式表示的版本信息.
        """
        async with self.session.get(self.url_gen("about")) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            version = (int(i) for i in data['data']['version'][1:].split("."))
            if auto_set:
                self.connect_info.current_version = version
            return version

    @applicationContextManager
    async def authenticate(self) -> str:
        """从路由 `/auth` 下获取尚未被激活的会话标识并返回; 通常的, 你还需要使用 `activeSession` 方法激活它.

        Returns:
            str: 即返回的会话标识
        """
        async with self.session.post(self.url_gen("auth"), json={
            "authKey": self.connect_info.authKey
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            self.connect_info.sessionKey = data['session']
            return data['session']

    @applicationContextManager
    async def activeSession(self) -> NoReturn:
        """激活当前已经存入 connect_info 的会话标识,
        如果没有事先调用 `authenticate` 方法获取未激活的会话标识, 则会触发 `InvaildSession` 错误.

        Raises:
            InvaildSession: 没有事先调用 `authenticate` 方法获取未激活的会话标识

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        if not self.connect_info.sessionKey:
            raise InvaildSession("you should call 'authenticate' before this to get a sessionKey!")
        async with self.session.post(self.url_gen("verify"), json={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def signout(self) -> NoReturn:
        """释放当前激活/未激活的会话标识

        Raises:
            InvaildSession: 没有事先调用 `authenticate` 方法获取会话标识

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        if not self.connect_info.sessionKey:
            raise InvaildSession("you should call 'authenticate' before this to get a sessionKey!")
        async with self.session.post(self.url_gen("release"), json={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            self.connect_info.sessionKey = None

            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def getGroup(self, group_id: int) -> Optional[Group]:
        """尝试从已知的群组唯一ID, 获取对应群组的信息; 可能返回 None.

        Args:
            group_id (int): 尝试获取的群组的唯一 ID.

        Returns:
            Group: 操作成功, 你得到了你应得的.
            None: 未能获取到.
        """
        data = await self.groupList()
        for i in data:
            if i.id == group_id:
                return i

    @requireAuthenticated
    @applicationContextManager
    async def groupList(self) -> List[Group]:
        """获取当前会话账号所加入的所有群组的信息.

        Returns:
            List[Group]: 当前会话账号所加入的所有群组的信息
        """
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
    @applicationContextManager
    async def getMember(self, group: Union[Group, int], member_id: int) -> Optional[Member]:
        """尝试从已知的群组唯一 ID 和已知的群组成员的 ID, 获取对应成员的信息; 可能返回 None.

        Args:
            group_id (Union[Group, int]): 已知的群组唯一 ID
            member_id (int): 已知的群组成员的 ID

        Returns:
            Member: 操作成功, 你得到了你应得的.
            None: 未能获取到.
        """
        data = await self.memberList(group)
        for i in data:
            if i.id == member_id:
                return i

    @requireAuthenticated
    @applicationContextManager
    async def memberList(self, group: Union[Group, int]) -> List[Member]:
        """获取群组中所有群组成员的信息

        Args:
            group (Union[Group, int]): 群组/群组ID

        Returns:
            List[Member]: 即群组中所有成员的可被获取到的信息.
        """
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
    @applicationContextManager
    async def friendList(self) -> List[Friend]:
        """获取当前会话账号所拥有的所有好友的信息

        Returns:
            List[Friend]: 当前会话账号所拥有的所有好友的信息
        """
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
    @applicationContextManager
    async def getFriend(self, friend_id: int) -> Optional[Friend]:
        """从已知的可能的好友 ID, 获取 Friend 实例.

        Args:
            friend_id (int): 已知的可能的好友 ID.

        Returns:
            Friend: 操作成功, 你得到了你应得的.
            None: 未能获取到.
        """
        data = await self.friendList()
        for i in data:
            if i.id == friend_id:
                return i

    @requireAuthenticated
    @applicationContextManager
    async def uploadImage(self, image_bytes: bytes, method: UploadMethods, return_external: bool = False) -> Union[Image, external.Image]:
        """上传一张图片到远端服务器, 需要提供: 图片的原始数据(bytes), 图片的上传类型; 你可以控制是否返回外部态的 Image 消息元素.

        Args:
            image_bytes (bytes): 图片的原始数据
            method (UploadMethods): 图片的上传类型
            return_external (bool, optional): 是否返回外部态的 Image 消息元素. 默认为 False.

        Returns:
            Image(internal): 内部态的 Image 消息元素
            Image(external): 外部态的 Image 消息元素
        """
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
    @applicationContextManager
    async def sendFriendMessage(self, target: Union[Friend, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        """发送消息给好友, 可以指定回复的消息.

        Args:
            target (Union[Friend, int]): 指定的好友
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.

        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.
        """
        with enter_message_send_context(UploadMethods.Friend):
            message_result = await message.build()
            async with self.session.post(self.url_gen("sendFriendMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "target": target.id if isinstance(target, Friend) else target,
                "messageChain": message_result.dict()['__root__'],
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info("[BOT {bot_id}] Friend({friend_id}) <- {message}".format_map({
                    "bot_id": self.connect_info.account,
                    "friend_id": target.id if isinstance(target, Friend) else target,
                    "message": message_result.asSerializationString()
                }))
                return BotMessage(messageId=data['messageId'])

    @requireAuthenticated
    @applicationContextManager
    async def sendGroupMessage(self, group: Union[Group, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        """发送消息到群组内, 可以指定回复的消息.

        Args:
            group (Union[Group, int]): 指定的群组, 可以是群组的 ID 也可以是 Group 实例.  
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.  
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.

        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.
        """
        with enter_message_send_context(UploadMethods.Group):
            message_result = await message.build()
            async with self.session.post(self.url_gen("sendGroupMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "messageChain": message_result.dict()['__root__'],
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info("[BOT {bot_id}] Group({group_id}) <- {message}".format_map({
                    "bot_id": self.connect_info.account,
                    "group_id": group.id if isinstance(group, Group) else group,
                    "message": message_result.asSerializationString()
                }))
                return BotMessage(messageId=data['messageId'])
    
    @requireAuthenticated
    @applicationContextManager
    async def sendTempMessage(self,
        group: Union[Group, int],
        target: Union[Member, int],
        message: MessageChain, *,
        quote: Optional[Union[Source, int]] = None
    ) -> BotMessage:
        """发送临时会话给群组中的特定成员, 可指定回复的消息.

        Args:
            group (Union[Group, int]): 指定的群组, 可以是群组的 ID 也可以是 Group 实例.
            target (Union[Member, int]): 指定的群组成员, 可以是成员的 ID 也可以是 Member 实例.
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.

        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.
        """
        message_result = await message.build()
        with enter_message_send_context(UploadMethods.Temp):
            async with self.session.post(self.url_gen("sendTempMessage"), json={
                "sessionKey": self.connect_info.sessionKey,
                "group": group.id if isinstance(group, Group) else group,
                "qq": target.id if isinstance(target, Member) else target,
                "messageChain": message_result.dict()['__root__'],
                **({
                    "quote": quote.id if isinstance(quote, Source) else quote
                } if quote else {})
            }) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info("[BOT {bot_id}] Member({member_id}, in {group_id}) <- {message}".format_map({
                    "bot_id": self.connect_info.account,
                    "member_id": target.id if isinstance(target, Member) else target,
                    "group_id": group.id if isinstance(group, Group) else group,
                    "message": message_result.asSerializationString()
                }))
                return BotMessage(messageId=data['messageId'])

    @requireAuthenticated
    @applicationContextManager
    async def revokeMessage(self,
        target: Union[Source, BotMessage, int]
    ) -> NoReturn:
        """撤回特定的消息; 撤回自己的消息需要在发出后 2 分钟内才能成功撤回; 如果在群组内, 需要撤回他人的消息则需要管理员/群主权限.

        Args:
            target (Union[Source, BotMessage, int]): 特定信息的 `messageId`, 可以是 `Source` 实例, `BotMessage` 实例或者是单纯的 int 整数.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        if isinstance(target, BotMessage):
            target = target.messageId
        elif isinstance(target, Source):
            target = target.id

        async with self.session.post(self.url_gen("recall"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": target
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
    
    @requireAuthenticated
    @applicationContextManager
    async def fetchMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        """从路由 `/fetchMessage` 处获取指定数量的消息; 当关闭 Websocket 时, 该方法被用于获取事件.

        Args:
            count (int, optional): 消息获取的数量. 默认为 10.

        Returns:
            List[Union[GroupMessage, TempMessage, FriendMessage]]: 获取到的消息
        """
        async with self.session.get(str(URL(self.url_gen("fetchMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for event in data['data']:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error("".join(["received a unknown event: ", event.get("type"), str(event)]))
                    continue
            return result
    
    @requireAuthenticated
    @applicationContextManager
    async def fetchLatestMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("fetchLatestMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for event in data['data']:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error("".join(["received a unknown event: ", event.get("type"), str(event)]))
                    continue
            return result

    @requireAuthenticated
    @applicationContextManager
    async def peekMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("peekMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for event in data['data']:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error("".join(["received a unknown event: ", event.get("type"), str(event)]))
                    continue
            return result
    
    @requireAuthenticated
    @applicationContextManager
    async def peekLatestMessage(self, count: int = 10) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(str(URL(self.url_gen("peekLatestMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "count": count
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            
            result = []
            for event in data['data']:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error("".join(["received a unknown event: ", event.get("type"), str(event)]))
                    continue
            return result

    @requireAuthenticated
    @applicationContextManager
    async def messageFromId(self, source: Union[Source, int]) -> Union[GroupMessage, TempMessage, FriendMessage]:
        """尝试从已知的 `messageId` 获取缓存中的消息

        Args:
            source (Union[Source, int]): 需要获取的消息的 `messageId`

        Returns:
            Union[GroupMessage, TempMessage, FriendMessage]: 获取到的消息
        """
        async with self.session.get(str(URL(self.url_gen("messageFromId")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "id": source.id if isinstance(source, Source) else source
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            try:
                return await self.auto_parse_by_type(event)
            except ValueError:
                self.logger.error("".join(["received a unknown event: ", event.get("type"), str(event)]))

    @requireAuthenticated
    @applicationContextManager
    async def countMessage(self) -> int:
        """获取 `mirai-api-http` 内部缓存中的消息的数量

        Returns:
            int: 缓存中的消息的数量
        """
        async with self.session.get(str(URL(self.url_gen("countMessage")).with_query({
            "sessionKey": self.connect_info.sessionKey,
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return data['data']

    @requireAuthenticated
    @applicationContextManager
    async def muteAll(self, group: Union[Group, int]) -> NoReturn:
        """在指定群组开启全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)

        Args:
            group (Union[Group, int]): 指定的群组.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(self.url_gen("muteAll"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def unmuteAll(self, group: Union[Group, int]) -> NoReturn:
        """在指定群组关闭全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)

        Args:
            group (Union[Group, int]): 指定的群组.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(self.url_gen("unmuteAll"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def mute(self, group: Union[Group, int], member: Union[Member, int], time: int) -> NoReturn:
        """在指定群组禁言指定群成员; 需要具有相应权限(管理员/群主); `time` 不得大于 `30*24*60*60=2592000` 或小于 `0`, 否则会自动修正;
        当 `time` 小于等于 `0` 时, 不会触发禁言操作; 禁言对象极有可能触发 `PermissionError`, 在这之前请对其进行判断!

        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
            time (int): 禁言事件, 单位秒, 修正规则: `{time|0 < time <= 2592000}`

        Raises:
            PermissionError: 没有相应操作权限.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        time = max(0, min(time, 2592000))
        if time == 0:
            return
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
    @applicationContextManager
    async def unmute(self, group: Union[Group, int], member: Union[Member, int]) -> NoReturn:
        """在指定群组解除对指定群成员的禁言; 需要具有相应权限(管理员/群主); 对象极有可能触发 `PermissionError`, 在这之前请对其进行判断!

        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)

        Raises:
            PermissionError: 没有相应操作权限.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(self.url_gen("unmute"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
    
    @requireAuthenticated
    @applicationContextManager
    async def kick(self, group: Union[Group, int], member: Union[Member, int], message: Optional[str] = None) -> NoReturn:
        """将目标群组成员从指定群组删除; 需要具有相应权限(管理员/群主)

        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
            message (Optional[str], optional): 如果给出, 则作为该操作的利益并向对象展示; 在当前版本中, 指定本参数无效. 默认为 None.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
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
    @applicationContextManager
    async def quit(self, group: Union[Group, int]) -> NoReturn:
        """主动从指定群组退出

        Args:
            group (Union[Group, int]): 需要退出的指定群组

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(self.url_gen("quit"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def getGroupConfig(self, group: Union[Group, int]) -> GroupConfig:
        """获取指定群组的群设置

        Args:
            group (Union[Group, int]): 需要获取群设置的指定群组

        Returns:
            GroupConfig: 指定群组的群设置
        """
        async with self.session.get(str(URL(self.url_gen("groupConfig")).with_query({
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return GroupConfig.parse_obj(data)

    @requireAuthenticated
    @applicationContextManager
    async def modifyGroupConfig(self, group: Union[Group, int], config: GroupConfig) -> NoReturn:
        """修改指定群组的群设置; 需要具有相应权限(管理员/群主).

        Args:
            group (Union[Group, int]): 需要修改群设置的指定群组
            config (GroupConfig): 经过修改后的群设置

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(self.url_gen("groupConfig"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "config": config.dict(exclude_none=True, exclude_unset=True, by_alias=True)
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def getMemberInfo(self, member: Union[Member, int], group: Optional[Union[Group, int]] = None) -> MemberInfo:
        """获取指定群组成员的可修改状态.

        Args:
            member (Union[Member, int]): 指定群成员, 可为 Member 实例, 若前设成立, 则不需要提供 group.
            group (Optional[Union[Group, int]], optional): 如果 member 为 Member 实例, 则不需要提供本项, 否则需要. 默认为 None.

        Raises:
            TypeError: 提供了错误的参数, 阅读有关文档得到问题原因

        Returns:
            MemberInfo: 指定群组成员的可修改状态
        """
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
    @applicationContextManager
    async def modifyMemberInfo(self, member: Union[Member, int], info: MemberInfo, group: Optional[Union[Group, int]] = None) -> NoReturn:
        """修改指定群组成员的可修改状态; 需要具有相应权限(管理员/群主).

        Args:
            member (Union[Member, int]): 指定的群组成员, 可为 Member 实例, 若前设成立, 则不需要提供 group.
            info (MemberInfo): 已修改的指定群组成员的可修改状态
            group (Optional[Union[Group, int]], optional): 如果 member 为 Member 实例, 则不需要提供本项, 否则需要. 默认为 None.

        Raises:
            TypeError: 提供了错误的参数, 阅读有关文档得到问题原因

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        if not group and not isinstance(member, Member):
            raise TypeError("you should give a Member instance if you cannot give a Group instance to me.")
        if isinstance(member, Member) and not group:
            group: Group = member.group
        async with self.session.post(self.url_gen("memberInfo"), json={
            "sessionKey": self.connect_info.sessionKey,
            "target": group.id if isinstance(group, Group) else group,
            "memberId": member.id if isinstance(member, Member) else member,
            "info": info.dict(exclude_none=True, exclude_unset=True, by_alias=True)
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @requireAuthenticated
    @applicationContextManager
    async def getConfig(self) -> MiraiConfig:
        """获取 mirai-api-http 中维护的当前会话的配置.

        Returns:
            MiraiConfig: 当前会话的配置
        """
        async with self.session.get(str(URL(self.url_gen("config")).with_query({
            "sessionKey": self.connect_info.sessionKey
        }))) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return MiraiConfig.parse_obj(data)

    @requireAuthenticated
    @applicationContextManager
    async def modifyConfig(self, *, cacheSize: Optional[int] = None, enableWebsocket: Optional[bool] = None) -> NoReturn:
        """修改当前会话的配置

        Args:
            cacheSize (Optional[int], optional): 缓存消息的条数. Defaults to None.
            enableWebsocket (Optional[bool], optional): 是否启用 Websocket 方式获取事件. Defaults to None.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
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
        """从尚未明确指定事件类型的对象中获取事件的定义, 并进行解析

        Args:
            original_dict (dict): 用 dict 表示的序列化态事件, 应包含有字段 `type` 以供分析事件定义.

        Raises:
            InvaildArgument: 目标对象中不包含字段 `type`
            ValueError: 没有找到对应的字段, 通常的, 这意味着应用获取到了一个尚未被定义的事件, 请报告问题.

        Returns:
            BaseEvent: 已经被序列化的事件
        """
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
                except TypeError:
                    continue
                if received_data:
                    if self.debug:
                        self.logger.debug("websocket received: " + str(received_data))
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
        """火箭升空叫 "launch", 只表示那一个阶段哦."""
        from .event.lifecycle import ApplicationLaunched, ApplicationLaunchedBlocking
        self.logger.info("launching app...")
        await self.authenticate()
        await self.activeSession()

        self.broadcast.postEvent(ApplicationLaunched(self))
        await self.broadcast.layered_scheduler(
            listener_generator=self.broadcast.default_listener_generator(ApplicationLaunchedBlocking),
            event=ApplicationLaunchedBlocking(self)
        )

        # 自动变化fetch方式
        fetch_method = self.http_fetchmessage_poster if not self.connect_info.websocket else self.ws_all_poster
        config: MiraiConfig = await self.getConfig()
        if not self.connect_info.websocket: # 不启用 websocket
            self.logger.info("using http to receive event")
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
            try:
                loop.run_until_complete(self.shutdown())
            except:
                self.logger.error("it seems our shutdown operator has been failed...check your headless client alive.")

    def subscribe_atexit(self, loop=None):
        """如果你需要使用 `create_background_task` 方法, 记得调用这个方法.

        Args:
            loop (asyncio.AbstractEventLoop, optional): 事件循环. Defaults to None.
        """
        loop = loop or self.broadcast.loop
        atexit.register(partial(loop.run_until_complete, self.shutdown()))

    def create_background_task(self, loop=None):
        """将获取事件并广播的协程创建为一个 Task, 放在事件循环里自己运行.

        Args:
            loop (asyncio.AbstractEventLoop, optional): 事件循环. Defaults to None.
        """
        loop = loop or self.broadcast.loop
        return loop.create_task(loop.run_until_complete(self.launch()))
