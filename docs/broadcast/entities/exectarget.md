Module graia.broadcast.entities.exectarget
==========================================

Classes
-------

`ExecTarget(callable: Callable, inline_dispatchers: List[Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]] = None, headless_decorators: List[graia.broadcast.entities.decorator.Decorator] = None, enable_internal_access: bool = False)`
:   

    ### Descendants

    * graia.broadcast.entities.listener.Listener

    ### Class variables

    `callable: Callable`
    :

    `enable_internal_access: bool`
    :

    `headless_decorators: List[graia.broadcast.entities.decorator.Decorator]`
    :

    `inline_dispatchers: List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]`
    :

    `maybe_failure: Set[str]`
    :

    `param_paths: Dict[str, List[List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]]]`
    :