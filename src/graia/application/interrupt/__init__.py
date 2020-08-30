from typing import Any, Type, Union
from pprint import pprint
from graia.broadcast import Broadcast
from graia.broadcast.priority import Priority
from graia.application import GraiaMiraiApplication
from graia.broadcast.entities.event import BaseEvent
from abc import ABCMeta, abstractmethod
from graia.broadcast.utilles import run_always_await
from graia.broadcast.entities.signatures import Force, RemoveMe
from graia.broadcast.exceptions import PropagationCancelled
import asyncio

class ActiveStats:
    def __init__(self) -> None:
        self.actived = False

    def get(self) -> bool:
        return self.actived
    
    def set(self) -> bool:
        self.actived = True
        return True

class Interrupt(metaclass=ABCMeta):
    """内置中断(Interrupt)机制中, 中断项的抽象实现, 需要重写 `trigger` 方法, 该方法接受一个 event 参数,
    该中断会被立刻回收.
    """
    direct: Type[BaseEvent]
    _return_value: Any = None
    _block_propagation: bool = False

    def set_return_value(self, value: Any):
        self._return_value = value

    def get_return_value(self):
        return self._return_value

    @abstractmethod
    def trigger(self, event: BaseEvent) -> Union[None, Any]:
        pass

class InterruptControl:
    """即中断控制, 主要是用于监听器/其他地方进行对符合特定要求的事件的捕获, 并返回事件.

    Methods:
        coroutine wait(interrupt: Interrupt) -> Any: 该方法主要用于在当前执行处堵塞当前协程,
            同时将一个一次性使用的监听器挂载, 只要获取到符合条件的事件, 该方法会通过你传入的 `Interrupt` 实例的方法 `trigger`,
            获取处理得到的值并返回; 无论如何, 用于一次性监听使用的监听器总会被销毁.
    """
    broadcast: Broadcast
    app: GraiaMiraiApplication

    def __init__(self, broadcast: Broadcast) -> None:
        self.broadcast = broadcast
    
    async def wait(self, interrupt: Interrupt, priority: Union[int, Priority, None] = None, **kwargs):
        """生成一一次性使用的监听器并将其挂载, 该监听器用于获取特定类型的事件, 并根据设定对事件进行过滤;
        当获取到符合条件的对象时, 堵塞将被解除, 同时该方法返回从监听器得到的值.

        Args:
            interrupt (Interrupt): 中断, 通常在 `graia.application.interrupt.interrupts` 下被定义.
            priority (Union[int, Priority, None]): 中断 inline 监听器的优先级, Defaults to None.
            **kwargs: 都会直接传入 Broadcast.receiver.

        Returns:
            Any: 通常这个值由中断本身定义并返回.
        """
        local_event = asyncio.Event()
        listener_callable = self.leader_listener_generator(local_event, interrupt)
        self.broadcast.receiver(interrupt.direct, priority=priority, **kwargs)(listener_callable)
        try:
            await local_event.wait()
        finally: # 删除 Listener
            if not local_event.is_set():
                self.broadcast.removeListener(self.broadcast.getListener(listener_callable))
        return interrupt.get_return_value()

    def leader_listener_generator(self, event_lock: asyncio.Event, interrupt: Interrupt):
        active_stat = ActiveStats()
        async def inside_listener(event: interrupt.direct):
            if active_stat.get():
                return RemoveMe()
            try:
                result = await run_always_await(interrupt.trigger(event))
                if result is not None:
                    active_stat.set()
                    event_lock.set()
                    if isinstance(result, Force):
                        result = result.target
                    interrupt.set_return_value(result)
                    if not interrupt._block_propagation:
                        return RemoveMe()
                    raise PropagationCancelled()
            except:
                import traceback
                traceback.print_exc()
        return inside_listener