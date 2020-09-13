from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

class SchedulerTaskExecute(BaseEvent):
    class Dispatcher(BaseDispatcher):
        def catch(interface: DispatcherInterface):
            pass