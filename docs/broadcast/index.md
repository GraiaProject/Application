Module graia.broadcast
======================

Sub-modules
-----------
* graia.broadcast.builtin
* graia.broadcast.entities
* graia.broadcast.exceptions
* graia.broadcast.interfaces
* graia.broadcast.interrupt
* graia.broadcast.priority
* graia.broadcast.typing
* graia.broadcast.utilles

Classes
-------

`Broadcast(*, loop: asyncio.events.AbstractEventLoop = None, debug_flag: bool = False)`
:   

    ### Class variables

    `debug_flag: bool`
    :

    `default_namespace: graia.broadcast.entities.namespace.Namespace`
    :

    `dispatcher_interface: graia.broadcast.interfaces.dispatcher.DispatcherInterface`
    :

    `listeners: List[graia.broadcast.entities.listener.Listener]`
    :

    `loop: asyncio.events.AbstractEventLoop`
    :

    `namespaces: List[graia.broadcast.entities.namespace.Namespace]`
    :

    ### Static methods

    `event_class_generator(target=graia.broadcast.entities.event.BaseEvent)`
    :

    `findEvent(name: str)`
    :

    ### Methods

    `Executor(self, target: Union[Callable, graia.broadcast.entities.exectarget.ExecTarget], event: graia.broadcast.entities.event.BaseEvent, dispatchers: List[Union[Type[graia.broadcast.entities.dispatcher.BaseDispatcher], Callable, graia.broadcast.entities.dispatcher.BaseDispatcher]] = None, post_exception_event: bool = False, print_exception: bool = True, enableInternalAccess: bool = False)`
    :

    `containListener(self, target)`
    :

    `containNamespace(self, name)`
    :

    `createNamespace(self, name, *, priority: int = 0, hide: bool = False, disabled: bool = False)`
    :

    `default_listener_generator(self, event_class) ‑> Iterable[graia.broadcast.entities.listener.Listener]`
    :

    `disableNamespace(self, name)`
    :

    `enableNamespace(self, name)`
    :

    `getDefaultNamespace(self)`
    :

    `getListener(self, target)`
    :

    `getNamespace(self, name)`
    :

    `hideNamespace(self, name)`
    :

    `layered_scheduler(self, listener_generator: Generator[graia.broadcast.entities.listener.Listener, NoneType, NoneType], event: graia.broadcast.entities.event.BaseEvent)`
    :

    `postEvent(self, event: graia.broadcast.entities.event.BaseEvent)`
    :

    `receiver(self, event: Union[str, Type[graia.broadcast.entities.event.BaseEvent]], priority: int = 16, dispatchers: List[Type[graia.broadcast.entities.dispatcher.BaseDispatcher]] = [], namespace: graia.broadcast.entities.namespace.Namespace = None, headless_decorators: List[graia.broadcast.entities.decorator.Decorator] = [], enable_internal_access: bool = False)`
    :

    `removeListener(self, target)`
    :

    `removeNamespace(self, name)`
    :

    `unhideNamespace(self, name)`
    :