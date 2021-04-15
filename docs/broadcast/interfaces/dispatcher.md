Module graia.broadcast.interfaces.dispatcher
============================================

Classes
-------

`DispatcherInterface(broadcast_instance: Broadcast)`
:   

    ### Class variables

    `broadcast: Broadcast`
    :

    `execution_contexts: List[ExecutionContext]`
    :

    `parameter_contexts: List[ParameterContext]`
    :

    `track_logs: List[graia.broadcast.entities.track_log.TrackLog]`
    :

    ### Static methods

    `dispatcher_callable_detector(dispatcher: Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]) ‑> Callable[[graia.broadcast.interfaces.dispatcher.DispatcherInterface], Any]`
    :

    `get_lifecycle_refs(dispatcher: T_Dispatcher) ‑> Union[Dict[str, List], NoneType]`
    :

    ### Instance variables

    `annotation: Any`
    :

    `current_path: graia.broadcast.utilles.NestableIterable[int, typing.Union[typing.Type[graia.broadcast.entities.dispatcher.BaseDispatcher], graia.broadcast.entities.dispatcher.BaseDispatcher, typing.Callable[[graia.broadcast.interfaces.dispatcher.DispatcherInterface], typing.Any]]]`
    :

    `default: Any`
    :

    `event: graia.broadcast.entities.event.BaseEvent`
    :

    `global_dispatcher: List[Union[Type[graia.broadcast.entities.dispatcher.BaseDispatcher], graia.broadcast.entities.dispatcher.BaseDispatcher, Callable[[graia.broadcast.interfaces.dispatcher.DispatcherInterface], Any]]]`
    :

    `has_current_exec_context: bool`
    :

    `has_current_param_context: bool`
    :

    `name: str`
    :

    `track_log`
    :

    ### Methods

    `dispatcher_pure_generator(self) ‑> Generator[NoneType, NoneType, Union[Type[graia.broadcast.entities.dispatcher.BaseDispatcher], graia.broadcast.entities.dispatcher.BaseDispatcher, Callable[[graia.broadcast.interfaces.dispatcher.DispatcherInterface], Any]]]`
    :

    `exec_lifecycle(self, lifecycle_name: str, *args, **kwargs)`
    :

    `exit_current_execution(self)`
    :

    `flush_lifecycle_refs(self, dispatchers: List[ForwardRef('T_Dispatcher')] = None)`
    :

    `init_dispatch_path(self) ‑> List[List[Union[Type[BaseDispatcher], BaseDispatcher, Callable[[DispatcherInterface], Any]]]]`
    :

    `inject_execution_raw(self, *dispatchers: List[ForwardRef('T_Dispatcher')])`
    :

    `inject_global_raw(self, *dispatchers: List[ForwardRef('T_Dispatcher')])`
    :

    `inject_local_raw(self, *dispatchers: List[ForwardRef('T_Dispatcher')])`
    :

    `lookup_by_directly(self, dispatcher: Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]], name: str, annotation: Any, default: Any, using_path: List[List[ForwardRef('T_Dispatcher')]] = None) ‑> Any`
    :

    `lookup_param(self, name: str, annotation: Any, default: Any, using_path: List[List[ForwardRef('T_Dispatcher')]] = None) ‑> Any`
    :

    `lookup_param_without_log(self, name: str, annotation: Any, default: Any, using_path: List[List[ForwardRef('T_Dispatcher')]] = None) ‑> Any`
    :

    `lookup_using_current(self) ‑> Any`
    :

    `start_execution(self, event: graia.broadcast.entities.event.BaseEvent, dispatchers: List[Union[Type[ForwardRef('BaseDispatcher')], ForwardRef('BaseDispatcher'), Callable[[ForwardRef('DispatcherInterface')], Any]]], track_log_receiver: graia.broadcast.entities.track_log.TrackLog = None) ‑> graia.broadcast.interfaces.dispatcher.DispatcherInterface`
    :

`EmptyEvent(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.