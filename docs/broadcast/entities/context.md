Module graia.broadcast.entities.context
=======================================

Functions
---------

    
`path_generator_factory(iterable: List[List[ForwardRef('T_Dispatcher')]], start: int)`
:   

Classes
-------

`ExecutionContext(dispatchers: List[Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]], event: BaseEvent)`
:   

    ### Class variables

    `dispatchers: List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]`
    :

    `event: BaseEvent`
    :

    `lifecycle_refs: Dict[str, List[Callable]]`
    :

`ParameterContext(name, annotation, default, dispatchers, using_path)`
:   

    ### Class variables

    `annotation: Any`
    :

    `default: Any`
    :

    `dispatchers: List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]`
    :

    `name: str`
    :