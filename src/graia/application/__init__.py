from typing import NoReturn, Optional, Tuple
from aiohttp import ClientSession
import asyncio
from graia.broadcast import Broadcast, broadcast
from graia.application.protocol.entities.session import Session
from graia.application.protocol.utilles import (
    raise_for_return_code, requireAuthenticated,
    SinceVersion
)
from graia.application.protocol.exceptions import(
    InvaildSession
)
import atexit
from yarl import URL

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
        async with self.session.post(self.url_gen("auth"), data={
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
        async with self.session.post(self.url_gen("verify"), data={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)

    async def signout(self) -> NoReturn:
        if not self.connect_info.sessionKey:
            raise InvaildSession("you should call 'authenticate' before this to get a sessionKey!")
        async with self.session.post(self.url_gen("release"), data={
            "sessionKey": self.connect_info.sessionKey,
            "qq": self.connect_info.account
        }) as response:
            response.raise_for_status()
            data = await response.json()
            raise_for_return_code(data)
        
    