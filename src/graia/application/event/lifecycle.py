from typing import Any
from graia.broadcast.entities.event import BaseEvent, BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from pydantic.main import BaseModel

class ApplicationLaunched(BaseModel, BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app

class ApplicationLaunchedBlocking(BaseModel, BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app

class ApplicationShutdowned(BaseModel, BaseEvent):
    app: Any

    def __init__(self, app) -> None:
        super().__init__(app=app)

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app

