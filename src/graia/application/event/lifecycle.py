from typing import Any
from graia.broadcast.entities.event import BaseEvent, BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from pydantic.main import BaseModel


class ApplicationLaunched(BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app


class ApplicationLaunchedBlocking(BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app


class ApplicationShutdowned(BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app
