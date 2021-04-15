Module graia.broadcast.interrupt
================================

Sub-modules
-----------
* graia.broadcast.interrupt.waiter

Classes
-------

`ActiveStats()`
:   

    ### Methods

    `get(self) ‑> bool`
    :

    `set(self) ‑> bool`
    :

`InterruptControl(broadcast: graia.broadcast.Broadcast)`
:   即中断控制, 主要是用于监听器/其他地方进行对符合特定要求的事件的捕获, 并返回事件.
    
    Methods:
        coroutine wait(interrupt: Interrupt) -> Any: 该方法主要用于在当前执行处堵塞当前协程,
            同时将一个一次性使用的监听器挂载, 只要获取到符合条件的事件, 该方法会通过你传入的 `Interrupt` 实例的方法 `trigger`,
            获取处理得到的值并返回; 无论如何, 用于一次性监听使用的监听器总会被销毁.

    ### Class variables

    `broadcast: graia.broadcast.Broadcast`
    :

    ### Methods

    `leader_listener_generator(self, event_lock: asyncio.locks.Event, waiter: graia.broadcast.interrupt.waiter.Waiter, event_type: Type[graia.broadcast.entities.event.BaseEvent], value_container: graia.broadcast.interrupt.Value, active_stat: graia.broadcast.interrupt.ActiveStats)`
    :

    `wait(self, waiter: graia.broadcast.interrupt.waiter.Waiter, priority: Union[int, graia.broadcast.priority.Priority, NoneType] = None, **kwargs)`
    :   生成一一次性使用的监听器并将其挂载, 该监听器用于获取特定类型的事件, 并根据设定对事件进行过滤;
        当获取到符合条件的对象时, 堵塞将被解除, 同时该方法返回从监听器得到的值.
        
        Args:
            waiter (Waiter): 等待器
            priority (Union[int, Priority]): 中断 inline 监听器的优先级, Defaults to 15.
            **kwargs: 都会直接传入 Broadcast.receiver.
        
        Returns:
            Any: 通常这个值由中断本身定义并返回.

`Value()`
:   

    ### Class variables

    `value: Any`
    :

    ### Methods

    `getValue(self) ‑> Any`
    :

    `setValue(self, value) ‑> NoneType`
    :