import asyncio
import atexit
from enum import Enum
import typing
from typing import List, NoReturn, Optional, Tuple, Union

from aiohttp import ClientSession
from aiohttp import FormData
from graia.application.protocol.entities.message.element.elements import (
    Image, ImageType)
from graia.application.protocol.entities.message.element.elements import external
from graia.application.protocol.entities.session import Session
from graia.application.protocol.exceptions import InvaildSession
from graia.application.protocol.utilles import (AppMiddlewareAsDispatcher,
                                                SinceVersion,
                                                raise_for_return_code,
                                                requireAuthenticated)
from graia.broadcast import Broadcast
from yarl import URL

from .protocol.entities.targets.friend import Friend
from .protocol import UploadMethods
from .protocol.entities.targets.group import Group, Member

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
        self.session = session or ClientSession()
        self.broadcast.getDefaultNamespace().injected_dispatchers.append(
            AppMiddlewareAsDispatcher()
        )
        atexit.register(self.close_session)

    def close_session(self):
        self.session.loop.run_until_complete(self.session.close())

    def url_gen(self, path) -> str:
        return str(URL(str(self.connect_info.host)).parent / path)
    
    @SinceVersion(1,6,2)
    async def getVersion(self, auto_set=True) -> Tuple:
        async with self.session.get(self.url_gen("about")) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data.get("code"))
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
        
    async def getGroup(self, group_id: int) -> Optional[Group]:
        data = await self.groupList()
        for i in data:
            if i.id == group_id:
                return i

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

    async def getMember(self, group: Union[Group, int], member_id: int) -> Member:
        data = await self.memberList(group)
        for i in data:
            if i.id == member_id:
                return i

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

    async def getFriend(self, friend_id: int) -> Friend:
        data = await self.friendList()
        for i in data:
            if i.id == friend_id:
                return i

    async def uploadImage(self, image_bytes: bytes, method: UploadMethods) -> Image:
        data = FormData()
        data.add_field("sessionKey", self.connect_info.sessionKey)
        data.add_field("type", method.value)
        data.add_field("img", image_bytes)
        async with self.session.post(self.url_gen("uploadImage"), data=data) as response:
            response.raise_for_status()
            resp_json = await response.json()
            raise_for_return_code(resp_json)
            return Image.parse_obj(external.Image.parse_obj(resp_json))