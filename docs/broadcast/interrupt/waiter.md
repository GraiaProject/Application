Module graia.broadcast.interrupt.waiter
=======================================

Classes
-------

`Waiter()`
:   

    ### Class variables

    `block_propagation: bool`
    :

    `enable_internal_access: bool`
    :

    `listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]]`
    :

    `priority: int`
    :

    `using_decorators: List[graia.broadcast.entities.decorator.Decorator]`
    :

    `using_dispatchers: List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]`
    :

    ### Static methods

    `create(listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]], using_dispatchers: List[Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]] = None, using_decorators: List[graia.broadcast.entities.decorator.Decorator] = None, priority: int = 15, enable_internal_access: bool = False, block_propagation: bool = False) ‑> Type[graia.broadcast.interrupt.waiter.Waiter]`
    :

    `create_using_function(listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]], using_dispatchers: List[Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]] = None, using_decorators: List[graia.broadcast.entities.decorator.Decorator] = None, priority: int = 15, enable_internal_access: bool = False, block_propagation: bool = False)`
    :

    ### Methods

    `detected_event(self) ‑> Any`
    :