Module graia.application.utilles
================================

Functions
---------

    
`DeprecatedSince(*version: int, action: str = 'warn')`
:   

    
`SinceVersion(*version: int)`
:   

    
`applicationContextManager(func: Callable)`
:   

    
`call_atonce(*args, **kwargs)`
:   

    
`context_enter_auto(context)`
:   

    
`print_traceback_javay()`
:   

    
`raise_for_return_code(code: Union[dict, int])`
:   

    
`requireAuthenticated(func: Callable)`
:   

    
`yes_or_no(value: bool) ‑> str`
:   

Classes
-------

`AppMiddlewareAsDispatcher(app)`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

    ### Class variables

    `always`
    :

    `context: AbstractContextManager`
    :

`AutoUnpackTuple(base_iterable: Iterable, pre_items: List[Any] = None)`
:   

`InsertGenerator(base_iterable: Iterable, pre_items: List[Any] = None)`
:   

    ### Descendants

    * graia.application.utilles.MultiUsageGenerator

    ### Class variables

    `base: Iterable[Any]`
    :

    `insert_items: List[Any]`
    :

`MultiUsageGenerator(base_iterable: Iterable, pre_items: List[Any] = None)`
:   

    ### Ancestors (in MRO)

    * graia.application.utilles.InsertGenerator

    ### Class variables

    `continue_count: int`
    :