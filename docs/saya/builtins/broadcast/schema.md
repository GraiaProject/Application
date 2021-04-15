Module graia.saya.builtins.broadcast.schema
===========================================

Classes
-------

`ListenerSchema(listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]], namespace: graia.broadcast.entities.namespace.Namespace = None, inline_dispatchers: List[graia.broadcast.entities.dispatcher.BaseDispatcher] = <factory>, headless_decorators: List[graia.broadcast.entities.decorator.Decorator] = <factory>, priority: int = 16, enable_internal_access: bool = False)`
:   ListenerSchema(listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]], namespace: graia.broadcast.entities.namespace.Namespace = None, inline_dispatchers: List[graia.broadcast.entities.dispatcher.BaseDispatcher] = <factory>, headless_decorators: List[graia.broadcast.entities.decorator.Decorator] = <factory>, priority: int = 16, enable_internal_access: bool = False)

    ### Ancestors (in MRO)

    * graia.saya.schema.BaseSchema

    ### Class variables

    `enable_internal_access: bool`
    :

    `headless_decorators: List[graia.broadcast.entities.decorator.Decorator]`
    :

    `inline_dispatchers: List[graia.broadcast.entities.dispatcher.BaseDispatcher]`
    :

    `listening_events: List[Type[graia.broadcast.entities.event.BaseEvent]]`
    :

    `namespace: graia.broadcast.entities.namespace.Namespace`
    :

    `priority: int`
    :

    ### Methods

    `build_listener(self, callable: Callable)`
    :