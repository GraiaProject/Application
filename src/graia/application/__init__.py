import asyncio
import atexit
import functools
import json
import time
import traceback
from contextlib import asynccontextmanager
from functools import partial
from typing import Any, Callable, List, NoReturn, Optional, Tuple, TypeVar, Union

import aiohttp.client_exceptions
import aiohttp.web_exceptions
import aiohttp.client_ws
import graia.application.event.mirai  # for init events
from aiohttp import ClientSession, FormData
from aiohttp.http_websocket import WSMsgType
from graia.application.event import MiraiEvent
from graia.application.event.lifecycle import (  # for init lifecycle events
    ApplicationLaunched,
    ApplicationLaunchedBlocking,
    ApplicationShutdowned,
)
from graia.broadcast import Broadcast
from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.utilles import printer, run_always_await
from yarl import URL

from graia.application.event.network import (
    RemoteException,
    SessionRefreshFailed,
    SessionRefreshed,
)
from graia.application.test.request_tracing import HttpRequestTracing

from .context import enter_context, enter_message_send_context
from .entities import MiraiConfig, UploadMethods
from .event.messages import FriendMessage, GroupMessage, TempMessage
from .exceptions import InvaildArgument, InvaildSession, NotSupportedVersion
from .friend import Friend
from .group import Group, GroupConfig, Member, MemberInfo, FileList, FileInfo
from .logger import AbstractLogger, LoggingLogger
from .message import BotMessage
from .message.chain import MessageChain
from .message.elements import external
from .message.elements.internal import Image, Source, Voice
from .session import Session
from .utilles import (
    AppMiddlewareAsDispatcher,
    SinceVersion,
    applicationContextManager,
    raise_for_return_code,
    requireAuthenticated,
    yes_or_no,
)


def error_wrapper(network_action_callable: Callable):
    @functools.wraps(network_action_callable)
    async def wrapped_network_action_callable(
        self: "GraiaMiraiApplication", *args, **kwargs
    ):
        running_count = 0

        while running_count < 5:
            running_count += 1
            try:
                return await network_action_callable(self, *args, **kwargs)
            except InvaildSession as invaild_session_exc:
                self.logger.error(
                    "Graia detected a invaild session, did you restart your mirai-console?"
                )
                self.logger.error(
                    "refreshing session after 5 seconds, because of an invaild session."
                )

                step_count = 0
                while step_count < 5:
                    step_count += 1
                    await asyncio.sleep(5)
                    self.logger.error("refreshing session...")
                    try:
                        await self.authenticate()
                        await self.activeSession()
                        await self.switch_event_detect_method()
                        self.broadcast.postEvent(SessionRefreshed())
                        break
                    except Exception as e:
                        self.logger.error(
                            "failed to refreshing session, we had retried {0} times, and we will have a try again.".format(
                                running_count
                            )
                        )
                        traceback.print_exc()
                        continue
                else:
                    self.logger.error(
                        "failed to refreshing session at last, so raise the error."
                    )
                    self.broadcast.postEvent(SessionRefreshFailed())
                    raise invaild_session_exc
            except aiohttp.web_exceptions.HTTPNotFound:
                raise NotSupportedVersion(
                    "{}: this action does not supported because remote returned 404.".format(
                        network_action_callable.__name__
                    )
                )
            except aiohttp.web_exceptions.HTTPInternalServerError as e:
                self.broadcast.postEvent(RemoteException())
                self.logger.error(
                    "the remote throwed a exception, please check the console!"
                )
                raise
            except (
                aiohttp.web_exceptions.HTTPMethodNotAllowed,
                aiohttp.web_exceptions.HTTPRequestURITooLong,
                aiohttp.web_exceptions.HTTPTooManyRequests,
            ):

                self.logger.error(
                    "ouch! it seems that we post in a wrong way for the action '{}', you should open a issue for Graia Application.".format(
                        network_action_callable.__name__
                    )
                )
                raise
            except aiohttp.web_exceptions.HTTPRequestTimeout:
                self.logger.error(
                    "timeout on {}, retry after 5 seconds...".format(
                        network_action_callable.__name__
                    )
                )
                await asyncio.sleep(5)
                continue

    return wrapped_network_action_callable


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
        "debug",
        "chat_log_enabled",
        "group_message_log_format",
        "friend_message_log_format",
        "temp_message_log_format",
        "json_loader",
    )

    broadcast: Optional[Broadcast]
    session: ClientSession
    connect_info: Session
    logger: AbstractLogger
    debug: bool
    chat_log_enabled: bool

    group_message_log_format: str
    friend_message_log_format: str
    temp_message_log_format: str

    json_loader: Callable[[Any], Any]

    def __init__(
        self,
        *,
        broadcast: Optional[Broadcast],
        connect_info: Session,
        session: Optional[ClientSession] = None,
        logger: Optional[AbstractLogger] = None,
        debug: bool = False,
        enable_chat_log: bool = True,
        group_message_log_format: str = "{bot_id}: [{group_name}({group_id})] {member_name}({member_id}) -> {message_string}",
        friend_message_log_format: str = "{bot_id}: [{friend_name}({friend_id})] -> {message_string}",
        temp_message_log_format: str = "{bot_id}: [{group_name}({group_id}.{member_name}({member_id})] -> {message_string}",
        json_loader: Callable[[Any], Any] = json.loads,
    ):
        self.broadcast = broadcast
        self.connect_info = connect_info
        self.logger = logger or LoggingLogger(**({"debug": True} if debug else {}))
        self.debug = debug
        self.session = session or ClientSession(loop=broadcast.loop)
        if debug:
            self.session = HttpRequestTracing(self.logger).build_session(self.session)

        self.chat_log_enabled = enable_chat_log

        if broadcast is not None:
            self.broadcast.dispatcher_interface.inject_global_raw(
                AppMiddlewareAsDispatcher(self)
            )
            if self.chat_log_enabled:
                self.broadcast.receiver("GroupMessage")(self.logger_group_message)
                self.broadcast.receiver("FriendMessage")(self.logger_friend_message)
                self.broadcast.receiver("TempMessage")(self.logger_temp_message)

        self.group_message_log_format = group_message_log_format
        self.friend_message_log_format = friend_message_log_format
        self.temp_message_log_format = temp_message_log_format

        self.json_loader = json_loader

    def logger_group_message(self, event: GroupMessage):
        self.logger.info(
            self.group_message_log_format.format_map(
                dict(
                    group_id=event.sender.group.id,
                    group_name=event.sender.group.name,
                    member_id=event.sender.id,
                    member_name=event.sender.name,
                    member_permission=event.sender.permission.name,
                    bot_id=self.connect_info.account,
                    bot_permission=event.sender.group.accountPerm.name,
                    message_string=event.messageChain.asSerializationString().__repr__(),
                )
            )
        )

    def logger_friend_message(self, event: FriendMessage):
        self.logger.info(
            self.friend_message_log_format.format_map(
                dict(
                    bot_id=self.connect_info.account,
                    friend_name=event.sender.nickname,
                    friend_id=event.sender.id,
                    message_string=event.messageChain.asSerializationString().__repr__(),
                )
            )
        )

    def logger_temp_message(self, event: TempMessage):
        self.logger.info(
            self.temp_message_log_format.format_map(
                dict(
                    group_id=event.sender.group.id,
                    group_name=event.sender.group.name,
                    member_id=event.sender.id,
                    member_name=event.sender.name,
                    member_permission=event.sender.permission.name,
                    bot_id=self.connect_info.account,
                    bot_permission=event.sender.group.accountPerm.name,
                    message_string=event.messageChain.asSerializationString().__repr__(),
                )
            )
        )

    def url_gen(self, path) -> str:
        """从 connect_info 和 path 生成接口的地址.

        Args:
            path (str): 需求的接口地址

        Returns:
            str: 作为结果的地址
        """
        return str(URL(str(self.connect_info.host)).parent / path)

    @SinceVersion(1, 6, 2)
    @error_wrapper
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

            version = tuple(
                int(i[1:] if i.startswith("v") else i)
                for i in data["data"]["version"].split(".")
            )
            if auto_set:
                self.connect_info.current_version = version
            return version

    @applicationContextManager
    async def authenticate(self) -> str:
        """从路由 `/auth` 下获取尚未被激活的会话标识并返回; 通常的, 你还需要使用 `activeSession` 方法激活它.

        Returns:
            str: 即返回的会话标识
        """
        async with self.session.post(
            self.url_gen("auth"), json={"authKey": self.connect_info.authKey}
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            self.connect_info.sessionKey = data["session"]
            return data["session"]

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
            raise InvaildSession(
                "you should call 'authenticate' before this to get a sessionKey!"
            )
        async with self.session.post(
            self.url_gen("verify"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "qq": self.connect_info.account,
            },
        ) as response:
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
            raise InvaildSession(
                "you should call 'authenticate' before this to get a sessionKey!"
            )
        async with self.session.post(
            self.url_gen("release"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "qq": self.connect_info.account,
            },
        ) as response:
            self.connect_info.sessionKey = None

            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
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

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def groupList(self) -> List[Group]:
        """获取当前会话账号所加入的所有群组的信息.

        Returns:
            List[Group]: 当前会话账号所加入的所有群组的信息
        """
        async with self.session.get(
            str(
                URL(self.url_gen("groupList")).with_query(
                    {"sessionKey": self.connect_info.sessionKey}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Group.parse_obj(i) for i in data]

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getMember(
        self, group: Union[Group, int], member_id: int
    ) -> Optional[Member]:
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

    @error_wrapper
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
            str(
                URL(self.url_gen("memberList")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                        "target": group.id if isinstance(group, Group) else group,
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Member.parse_obj(i) for i in data]

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def friendList(self) -> List[Friend]:
        """获取当前会话账号所拥有的所有好友的信息

        Returns:
            List[Friend]: 当前会话账号所拥有的所有好友的信息
        """
        async with self.session.get(
            str(
                URL(self.url_gen("friendList")).with_query(
                    {"sessionKey": self.connect_info.sessionKey}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [Friend.parse_obj(i) for i in data]

    @error_wrapper
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

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def uploadImage(
        self, image_bytes: bytes, method: UploadMethods, return_external: bool = False
    ) -> Union[Image, external.Image]:
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
        async with self.session.post(
            self.url_gen("uploadImage"), data=data
        ) as response:
            response.raise_for_status()
            resp_json = await response.json()
            raise_for_return_code(resp_json)
            external_component = external.Image.parse_obj(resp_json)
            if return_external:
                return external_component
            else:
                return Image.fromExternal(external_component)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def uploadVoice(
        self,
        voice_bytes: bytes,
        method: UploadMethods = UploadMethods.Group,
        return_external: bool = False,
    ) -> Union[Voice, external.Voice]:
        """上传一份语音数据(类型为原始 bytes)到远端服务器, 需要提供: 语音的原始数据(bytes), 语音的上传类型(默认为 Group); 你可以控制是否返回外部态的 Voice 消息元素.

        Args:
            voice_bytes (bytes): 语音的原始数据
            method (UploadMethods): 语音的上传类型, 默认为 `UploadMethods.Group`.
            return_external (bool, optional): 是否返回外部态的 Voice 消息元素. 默认为 False.

        Returns:
            Voice(internal): 内部态的 Voice 消息元素
            Voice(external): 外部态的 Voice 消息元素
        """
        data = FormData()
        data.add_field("sessionKey", self.connect_info.sessionKey)
        data.add_field("type", method.value)
        data.add_field("voice", voice_bytes)
        async with self.session.post(
            self.url_gen("uploadVoice"), data=data
        ) as response:
            response.raise_for_status()
            resp_json = await response.json()
            raise_for_return_code(resp_json)
            external_component = external.Voice.parse_obj(resp_json)
            if return_external:
                return external_component
            else:
                return Voice.fromExternal(external_component)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def sendFriendMessage(
        self,
        target: Union[Friend, int],
        message: MessageChain,
        *,
        quote: Optional[Union[Source, int]] = None,
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
            async with self.session.post(
                self.url_gen("sendFriendMessage"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "target": target.id if isinstance(target, Friend) else target,
                    "messageChain": message_result.dict()["__root__"],
                    **(
                        {"quote": quote.id if isinstance(quote, Source) else quote}
                        if quote
                        else {}
                    ),
                },
            ) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info(
                    "[BOT {bot_id}] Friend({friend_id}) <- {message}".format_map(
                        {
                            "bot_id": self.connect_info.account,
                            "friend_id": target.id
                            if isinstance(target, Friend)
                            else target,
                            "message": message_result.asSerializationString().__repr__(),
                        }
                    )
                )
                return BotMessage(messageId=data["messageId"])

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def sendGroupMessage(
        self,
        group: Union[Group, int],
        message: MessageChain,
        *,
        quote: Optional[Union[Source, int]] = None,
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
            async with self.session.post(
                self.url_gen("sendGroupMessage"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "target": group.id if isinstance(group, Group) else group,
                    "messageChain": message_result.dict()["__root__"],
                    **(
                        {"quote": quote.id if isinstance(quote, Source) else quote}
                        if quote
                        else {}
                    ),
                },
            ) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info(
                    "[BOT {bot_id}] Group({group_id}) <- {message}".format_map(
                        {
                            "bot_id": self.connect_info.account,
                            "group_id": group.id if isinstance(group, Group) else group,
                            "message": message_result.asSerializationString().__repr__(),
                        }
                    )
                )
                return BotMessage(messageId=data["messageId"])

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def sendTempMessage(
        self,
        group: Union[Group, int],
        target: Union[Member, int],
        message: MessageChain,
        *,
        quote: Optional[Union[Source, int]] = None,
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
            async with self.session.post(
                self.url_gen("sendTempMessage"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "group": group.id if isinstance(group, Group) else group,
                    "qq": target.id if isinstance(target, Member) else target,
                    "messageChain": message_result.dict()["__root__"],
                    **(
                        {"quote": quote.id if isinstance(quote, Source) else quote}
                        if quote
                        else {}
                    ),
                },
            ) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

                self.logger.info(
                    "[BOT {bot_id}] Member({member_id}, in {group_id}) <- {message}".format_map(
                        {
                            "bot_id": self.connect_info.account,
                            "member_id": target.id
                            if isinstance(target, Member)
                            else target,
                            "group_id": group.id if isinstance(group, Group) else group,
                            "message": message_result.asSerializationString().__repr__(),
                        }
                    )
                )
                return BotMessage(messageId=data["messageId"])

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def revokeMessage(self, target: Union[Source, BotMessage, int]) -> NoReturn:
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

        async with self.session.post(
            self.url_gen("recall"),
            json={"sessionKey": self.connect_info.sessionKey, "target": target},
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def fetchMessage(
        self, count: int = 10
    ) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        """从路由 `/fetchMessage` 处获取指定数量的消息; 当关闭 Websocket 时, 该方法被用于获取事件.

        Args:
            count (int, optional): 消息获取的数量. 默认为 10.

        Returns:
            List[Union[GroupMessage, TempMessage, FriendMessage]]: 获取到的消息
        """
        async with self.session.get(
            str(
                URL(self.url_gen("fetchMessage")).with_query(
                    {"sessionKey": self.connect_info.sessionKey, "count": count}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            result = []
            for event in data["data"]:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error(
                        "".join(
                            [
                                "received a unknown event: ",
                                event.get("type"),
                                str(event),
                            ]
                        )
                    )
                    continue
            return result

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def fetchLatestMessage(
        self, count: int = 10
    ) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(
            str(
                URL(self.url_gen("fetchLatestMessage")).with_query(
                    {"sessionKey": self.connect_info.sessionKey, "count": count}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            result = []
            for event in data["data"]:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error(
                        "".join(
                            [
                                "received a unknown event: ",
                                event.get("type"),
                                str(event),
                            ]
                        )
                    )
                    continue
            return result

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def peekMessage(
        self, count: int = 10
    ) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(
            str(
                URL(self.url_gen("peekMessage")).with_query(
                    {"sessionKey": self.connect_info.sessionKey, "count": count}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            result = []
            for event in data["data"]:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error(
                        "".join(
                            [
                                "received a unknown event: ",
                                event.get("type"),
                                str(event),
                            ]
                        )
                    )
                    continue
            return result

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def peekLatestMessage(
        self, count: int = 10
    ) -> List[Union[GroupMessage, TempMessage, FriendMessage]]:
        async with self.session.get(
            str(
                URL(self.url_gen("peekLatestMessage")).with_query(
                    {"sessionKey": self.connect_info.sessionKey, "count": count}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            result = []
            for event in data["data"]:
                if self.debug:
                    self.logger.debug("http polling received: " + str(event))
                try:
                    result.append(await self.auto_parse_by_type(event))
                except ValueError:
                    self.logger.error(
                        "".join(
                            [
                                "received a unknown event: ",
                                event.get("type"),
                                str(event),
                            ]
                        )
                    )
                    continue
            return result

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def messageFromId(
        self, source: Union[Source, int]
    ) -> Union[GroupMessage, TempMessage, FriendMessage]:
        """尝试从已知的 `messageId` 获取缓存中的消息

        Args:
            source (Union[Source, int]): 需要获取的消息的 `messageId`

        Returns:
            Union[GroupMessage, TempMessage, FriendMessage]: 获取到的消息
        """
        async with self.session.get(
            str(
                URL(self.url_gen("messageFromId")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                        "id": source.id if isinstance(source, Source) else source,
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            try:
                return await self.auto_parse_by_type(data["data"])
            except ValueError:
                self.logger.error(
                    "".join(
                        [
                            "received a unknown event: ",
                            data["data"].get("type"),
                            str(data),
                        ]
                    )
                )

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def countMessage(self) -> int:
        """获取 `mirai-api-http` 内部缓存中的消息的数量

        Returns:
            int: 缓存中的消息的数量
        """
        async with self.session.get(
            str(
                URL(self.url_gen("countMessage")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return data["data"]

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def muteAll(self, group: Union[Group, int]) -> NoReturn:
        """在指定群组开启全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)

        Args:
            group (Union[Group, int]): 指定的群组.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("muteAll"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def unmuteAll(self, group: Union[Group, int]) -> NoReturn:
        """在指定群组关闭全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)

        Args:
            group (Union[Group, int]): 指定的群组.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("unmuteAll"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def mute(
        self, group: Union[Group, int], member: Union[Member, int], time: int
    ) -> NoReturn:
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
        async with self.session.post(
            self.url_gen("mute"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "memberId": member.id if isinstance(member, Member) else member,
                "time": time,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def unmute(
        self, group: Union[Group, int], member: Union[Member, int]
    ) -> NoReturn:
        """在指定群组解除对指定群成员的禁言; 需要具有相应权限(管理员/群主); 对象极有可能触发 `PermissionError`, 在这之前请对其进行判断!

        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)

        Raises:
            PermissionError: 没有相应操作权限.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("unmute"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "memberId": member.id if isinstance(member, Member) else member,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def kick(
        self,
        group: Union[Group, int],
        member: Union[Member, int],
        message: Optional[str] = None,
    ) -> NoReturn:
        """将目标群组成员从指定群组删除; 需要具有相应权限(管理员/群主)

        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
            message (Optional[str], optional): 如果给出, 则作为该操作的利益并向对象展示; 在当前版本中, 指定本参数无效. 默认为 None.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("kick"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "memberId": member.id if isinstance(member, Member) else member,
                **({"msg": message} if message else {}),
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def quit(self, group: Union[Group, int]) -> NoReturn:
        """主动从指定群组退出

        Args:
            group (Union[Group, int]): 需要退出的指定群组

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("quit"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getGroupConfig(self, group: Union[Group, int]) -> GroupConfig:
        """获取指定群组的群设置

        Args:
            group (Union[Group, int]): 需要获取群设置的指定群组

        Returns:
            GroupConfig: 指定群组的群设置
        """
        async with self.session.get(
            str(
                URL(self.url_gen("groupConfig")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                        "target": group.id if isinstance(group, Group) else group,
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return GroupConfig.parse_obj(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def modifyGroupConfig(
        self, group: Union[Group, int], config: GroupConfig
    ) -> NoReturn:
        """修改指定群组的群设置; 需要具有相应权限(管理员/群主).

        Args:
            group (Union[Group, int]): 需要修改群设置的指定群组
            config (GroupConfig): 经过修改后的群设置

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        async with self.session.post(
            self.url_gen("groupConfig"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "config": config.dict(
                    exclude_none=True, exclude_unset=True, by_alias=True
                ),
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getMemberInfo(
        self, member: Union[Member, int], group: Optional[Union[Group, int]] = None
    ) -> MemberInfo:
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
            raise TypeError(
                "you should give a Member instance if you cannot give a Group instance to me."
            )
        if isinstance(member, Member) and not group:
            group: Group = member.group
        async with self.session.get(
            str(
                URL(self.url_gen("memberInfo")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                        "target": group.id if isinstance(group, Group) else group,
                        "memberId": member.id if isinstance(member, Member) else member,
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return MemberInfo.parse_obj(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def modifyMemberInfo(
        self,
        member: Union[Member, int],
        info: MemberInfo,
        group: Optional[Union[Group, int]] = None,
    ) -> NoReturn:
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
            raise TypeError(
                "you should give a Member instance if you cannot give a Group instance to me."
            )
        if isinstance(member, Member) and not group:
            group: Group = member.group
        async with self.session.post(
            self.url_gen("memberInfo"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": group.id if isinstance(group, Group) else group,
                "memberId": member.id if isinstance(member, Member) else member,
                "info": info.dict(exclude_none=True, exclude_unset=True, by_alias=True),
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getConfig(self) -> MiraiConfig:
        """获取 mirai-api-http 中维护的当前会话的配置.

        Returns:
            MiraiConfig: 当前会话的配置
        """
        async with self.session.get(
            str(
                URL(self.url_gen("config")).with_query(
                    {"sessionKey": self.connect_info.sessionKey}
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

            return MiraiConfig.parse_obj(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def modifyConfig(
        self, *, cacheSize: Optional[int] = None, enableWebsocket: Optional[bool] = None
    ) -> NoReturn:
        """修改当前会话的配置

        Args:
            cacheSize (Optional[int], optional): 缓存消息的条数. Defaults to None.
            enableWebsocket (Optional[bool], optional): 是否启用 Websocket 方式获取事件. Defaults to None.

        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.
        """
        if any([cacheSize is not None, enableWebsocket is not None]):
            async with self.session.post(
                self.url_gen("config"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    **({"cacheSize": cacheSize} if cacheSize is not None else {}),
                    **(
                        {"enableWebsocket": enableWebsocket}
                        if enableWebsocket is not None
                        else {}
                    ),
                },
            ) as response:
                response.raise_for_status()
                data = await response.json()
                raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def setEssence(self, target: Union[BotMessage, Source, int]):
        """设置群精华消息, 需要机器人账号具有管理员及以上权限

        Args:
            target (Union[BotMessage, Source, int]): 将被设置为群精华消息的消息 Id (Message ID)
        """
        async with self.session.post(
            self.url_gen("setEssence"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": target.id
                if isinstance(target, (BotMessage, Source))
                else target,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def nudge(self, target: Union[Member, Friend]):
        async with self.session.post(
            self.url_gen("sendNudge"),
            json={
                "sessionKey": self.connect_info.sessionKey,
                "target": target.id,
                "subject": target.group.id if isinstance(target, Member) else target.id,
                "kind": {Member: "Group", Friend: "Friend"}[target.__class__],
            },
        ) as response:
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
        if not original_dict.get("type") and not isinstance(
            original_dict.get("type"), str
        ):
            raise InvaildArgument(
                "you need to provide a 'type' field for automatic parsing"
            )
        event_type = Broadcast.findEvent(original_dict.get("type"))
        if not event_type:
            raise ValueError(
                "we cannot find a such event: {}".format(original_dict.get("type"))
            )
        return await run_always_await(
            event_type.parse_obj(
                {k: v for k, v in original_dict.items() if k != "type"}
            )
        )

    async def ws_ping(
        self, ws_connect: aiohttp.client_ws.ClientWebSocketResponse, delay: float = 30.0
    ):
        while True:
            try:
                await ws_connect.ping()
                self.logger.debug("websocket ping: client ping")
            except asyncio.CancelledError:
                self.logger.debug("websocket ping: exiting....")
                return
            except:
                self.logger.exception("websocket ping: ping failed")
            self.logger.debug("websocket ping: delay {0}s.".format(delay))
            await asyncio.sleep(delay)

    @error_wrapper
    @requireAuthenticated
    async def ws_all_poster(self):
        ping_task = None

        async with self.session.ws_connect(
            str(
                URL(self.url_gen("all")).with_query(
                    {"sessionKey": self.connect_info.sessionKey}
                )
            ),
            autoping=False,
        ) as connection:
            self.logger.info("websocket: connected")

            ping_task = self.broadcast.loop.create_task(self.ws_ping(connection))
            self.logger.info("websocket: ping task created")

            try:
                while True:
                    ws_message = await connection.receive()
                    if ws_message.type is WSMsgType.TEXT:
                        received_data = self.json_loader(ws_message.data)
                        raise_for_return_code(received_data)

                        try:
                            event = await self.auto_parse_by_type(received_data)
                        except ValueError as e:
                            traceback.print_exc()
                            self.logger.error(
                                "".join(
                                    [
                                        "received a unknown event: ",
                                        received_data.get("type"),
                                        str(received_data),
                                    ]
                                )
                            )
                            continue

                        if self.debug:
                            self.logger.debug(f"websocket received: {event}")

                        with enter_context(app=self, event_i=event):
                            self.broadcast.postEvent(event)
                    elif ws_message.type is WSMsgType.CLOSED:
                        self.logger.info("websocket: connection has been closed.")
                        return
                    elif ws_message.type is WSMsgType.PONG:
                        self.logger.debug("websocket: received pong from remote")
                    else:
                        self.logger.debug(
                            "detected a unknown message type: {}".format(
                                ws_message.type
                            )
                        )
            finally:
                if ping_task:
                    ping_task.cancel()
                    self.logger.debug("websocket: outer canceled ping task")

    async def websocket_daemon(self):
        while True:
            self.logger.info("websocket daemon: websocket connection starting...")
            try:
                await self.ws_all_poster()
            except aiohttp.client_exceptions.ClientConnectorError:
                self.logger.info(
                    "websocket daemon: it seems that remote down, waiting for 10 seconds..."
                )
                await asyncio.sleep(10)
            self.logger.info("websocket daemon: detected closed, restarting...")

    @requireAuthenticated
    async def http_fetchmessage_poster(self, delay=0.5, fetch_num=10):
        while True:
            await asyncio.sleep(delay)
            while True:
                data = await self.fetchMessage(fetch_num)
                for i in data:
                    with enter_context(app=self, event_i=i):
                        self.broadcast.postEvent(i)
                if len(data) != fetch_num:
                    break

    async def switch_event_detect_method(self):
        config = await self.getConfig()
        if not self.connect_info.websocket:  # 不启用 websocket
            self.logger.info("using http to receive event")
            if config.enableWebsocket:  # 配置中已经启用
                await self.modifyConfig(enableWebsocket=False)
                self.logger.info("found websocket enabled, so it has been disabled.")
        else:  # 启用ws
            self.logger.info("using pure websocket to receive event")
            if not config.enableWebsocket:  # 配置中没启用
                self.logger.info("found websocket disabled, so it has been enabled.")
                await self.modifyConfig(enableWebsocket=True)

    async def initialize(self):
        start_time = time.time()
        self.logger.info("initializing app...")
        await self.authenticate()
        await self.activeSession()

        if self.broadcast is not None:
            self.broadcast.postEvent(ApplicationLaunched(self))
            await self.broadcast.layered_scheduler(
                listener_generator=self.broadcast.default_listener_generator(
                    ApplicationLaunchedBlocking
                ),
                event=ApplicationLaunchedBlocking(self),
            )

        self.logger.info("detecting remote's version...")
        try:
            await self.getVersion()
        except:
            self.logger.error("| failed to detect remote's version. |")
            self.logger.error("| it seems that your version is less than 1.6.2, |")
            self.logger.error(
                "| this version of Graia Application may cause many issues, |"
            )
            self.logger.error(
                "| so you had better to update your remote environment, |"
            )
            self.logger.error("| or you won't get our support! |")
            traceback.print_exc()
        else:
            self.logger.info(
                "detected remote's version: {0}".format(
                    ".".join(map(str, self.connect_info.current_version))
                )
            )

        # 自动变化fetch方式
        await self.switch_event_detect_method()

        self.logger.info("event receive method checked.")
        self.logger.info("this application's initialization has been completed.")

        self.logger.info("--- setting start ---")
        self.logger.info("broadcast using: {0}".format(self.broadcast.__repr__()))
        self.logger.info(
            "enable log of chat: {0}".format(yes_or_no(self.chat_log_enabled))
        )
        self.logger.info("debug: {0}".format(yes_or_no(self.debug)))
        self.logger.info(
            "version(remote): {0}".format(
                ".".join(map(str, self.connect_info.current_version))
            )
            if self.connect_info.current_version is not None
            else "No Detect"
        )
        self.logger.info("--- setting end ---")

        if not self.broadcast:
            self.logger.warn("it seems you doesn't offer a Broadcast,")
            self.logger.warn(
                "so the event receiver and the shutdown function won't launch!"
            )

        self.logger.info(
            "application has been initialized, used {0:.3}s".format(
                (time.time() - start_time)
            )
        )

    def getFetching(self):
        return (
            self.http_fetchmessage_poster
            if not self.connect_info.websocket
            else self.websocket_daemon
        )

    async def shutdown(self):
        if self.broadcast is not None:
            loop = self.broadcast.loop
            try:
                await self.broadcast.layered_scheduler(
                    listener_generator=self.broadcast.default_listener_generator(
                        ApplicationShutdowned
                    ),
                    event=ApplicationShutdowned(self),
                )
            except:
                self.logger.error(
                    "it seems our shutdown operator has been failed...check the remote alive."
                )
                traceback.print_exc()
        else:
            loop = asyncio.get_event_loop()

        for t in asyncio.all_tasks(loop):
            if t is not asyncio.current_task(loop):
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass

        await self.signout()
        await self.session.close()
        self.logger.info("application shutdowned.")

    def launch_blocking(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        if self.broadcast:
            loop = self.broadcast.loop
        else:
            loop = loop or asyncio.get_event_loop()

        if not self.connect_info.sessionKey:
            loop.run_until_complete(self.initialize())

        try:
            if self.broadcast:
                loop.run_until_complete(self.getFetching()())
        finally:
            if self.broadcast:
                loop.run_until_complete(self.shutdown())

    def initializeFetchingTask(self) -> asyncio.Task:
        if not self.broadcast:
            raise TypeError("if you want to use fetching, you must setup a Broadcast.")
        loop = self.broadcast.loop
        return loop.create_task(self.getFetching()())

    async def __aenter__(self) -> "GraiaMiraiApplication":
        await self.authenticate()
        await self.activeSession()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            await self.signout()
        except:
            pass

        if tb is not None:
            raise exc

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getGroupFileList(self, group: Union[Group, int], path: Optional[str] = None) -> List[FileList]:
        """获取指定群组中文件列表

        Args:
            group (Union[Group, int]): 需要获取的指定群组
            path (str): 指定文件目录，如果寻找根目录则不需要提供本项，默认为 None

        Returns:
            List[FileList]: 获得的文件列表.
        """
        async with self.session.get(
            str(
                URL(self.url_gen("groupFileList")).with_query(
                    {
                        "sessionKey": self.connect_info.sessionKey,
                        "target": group.id if isinstance(group, Group) else group,
                        "dir": path or ''
                    }
                )
            )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return [FileList.parse_obj(i) for i in data]

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def getGroupFileInfo(self, group: Union[Group, int], file_id: str) -> FileInfo:
        """获取指定群文件详细信息

        Args:
            group (Union[Group, int]): 需要获取的指定群组
            file_id (str): 指定文件的唯一标识符，从 getGroupFileList 方法获得

        Returns:
            FileInfo: 获得的文件详情.
        """
        async with self.session.get(
                str(
                    URL(self.url_gen("groupFileInfo")).with_query(
                        {
                            "sessionKey": self.connect_info.sessionKey,
                            "target": group.id if isinstance(group, Group) else group,
                            "id": file_id
                        }
                    )
                )
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
            return FileInfo.parse_obj(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def renameGroupFile(self, group: Union[Group, int], file_id: str, rename: str) -> NoReturn:
        """重命名群文件或目录

        Args:
            group (Union[Group, int]): 需要获取的指定群组
            file_id (str): 指定文件的唯一标识符，从 getGroupFileList 方法获得
            rename (str): 指定文件更名后的名称，需要加上文件后缀
        """
        async with self.session.post(
                self.url_gen("groupFileRename"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "target": group.id if isinstance(group, Group) else group,
                    "id": file_id,
                    "rename": rename
                }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def moveGroupFile(self, group: Union[Group, int], file_id: str, move_to: str) -> NoReturn:
        """移动群文件(目前疑似 Mirai-Api—Http 1.11.0 存在 bug，返回状态码 200 但文件未能移动)

        Args:
            group (Union[Group, int]): 需要获取的指定群组
            file_id (str): 指定文件的唯一标识符，从 getGroupFileList 方法获得
            move_to (str): 指定文件需要移动到的目录即 '/move_to', 目录不存在则自动创建
        """
        async with self.session.post(
                self.url_gen("groupFileMove"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "target": group.id if isinstance(group, Group) else group,
                    "id": file_id,
                    "movePath": move_to
                }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    @error_wrapper
    @requireAuthenticated
    @applicationContextManager
    async def removeGroupFile(self, group: Union[Group, int], file_id: str) -> NoReturn:
        """删除群文件或目录

        Args:
            group (Union[Group, int]): 需要获取的指定群组
            file_id (str): 指定文件的唯一标识符，从 getGroupFileList 方法获得
        """
        async with self.session.post(
                self.url_gen("groupFileDelete"),
                json={
                    "sessionKey": self.connect_info.sessionKey,
                    "target": group.id if isinstance(group, Group) else group,
                    "id": file_id
                }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
