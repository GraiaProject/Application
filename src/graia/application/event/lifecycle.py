from typing import Any
import typing
from graia.broadcast.entities.event import Dispatchable
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

if typing.TYPE_CHECKING:
    from graia.application import GraiaMiraiApplication

class ApplicationLaunched(Dispatchable):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app


class ApplicationLaunchedBlocking(Dispatchable):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app


class ApplicationShutdowned(Dispatchable):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app
