from graia.broadcast.entities.event import BaseEvent, BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

class ApplicationLaunched(BaseEvent):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app

class ApplicationLaunchedBlocking(BaseEvent):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app

class ApplicationShutdowned(BaseEvent):
    app: "GraiaMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        def catch(interface: "DispatcherInterface"):
            from .. import GraiaMiraiApplication
            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app