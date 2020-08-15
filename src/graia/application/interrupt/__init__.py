from typing import Any, Type, Union
from pprint import pprint
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.broadcast.entities.event import BaseEvent
from abc import ABCMeta, abstractmethod
from graia.broadcast.utilles import run_always_await
from graia.broadcast.entities.signatures import RemoveMe
import asyncio

class Interrupt(metaclass=ABCMeta):
    """内置中断(Interrupt)机制中, 中断项的抽象实现, 需要重写 `trigger` 方法, 该方法接受一个 event 参数,
    该中断会被立刻回收.
    """
    direct: Type[BaseEvent]
    _return_value: Any = None

    def set_return_value(self, value: Any):
        self._return_value = value

    def get_return_value(self):
        return self._return_value

    @abstractmethod
    def trigger(self, event: BaseEvent) -> Union[None, Any]:
        pass

class InterruptControl:
    broadcast: Broadcast
    app: GraiaMiraiApplication

    def __init__(self, broadcast: Broadcast) -> None:
        self.broadcast = broadcast
    
    async def wait(self, interrupt: Interrupt):
        local_event = asyncio.Event()
        listener_callable = self.leader_listener_generator(local_event, interrupt)
        self.broadcast.receiver(interrupt.direct)(listener_callable)
        try:
            await local_event.wait()
        finally: # 删除 Listener
            if not local_event.is_set():
                self.broadcast.removeListener(self.broadcast.getListener(listener_callable))
        return interrupt.get_return_value()

    def leader_listener_generator(self, event_lock: asyncio.Event, interrupt: Interrupt):
        async def inside_listener(event: interrupt.direct):
            try:
                result = await run_always_await(interrupt.trigger(event))
                if result is not None:
                    event_lock.set()
                    interrupt.set_return_value(result)
                    return RemoveMe()
            except:
                import traceback
                traceback.print_exc()
        return inside_listener