Module graia.broadcast.builtin.factory
======================================

Classes
-------

`AsyncDispatcherContextManager(generator_factory: Callable, args=None, kwargs=None)`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

    ### Descendants

    * graia.application.message.parser.kanata.Kanata

    ### Class variables

    `generator: AsyncGenerator[Union[NoneType, Tuple[Literal[<ResponseCodeEnum.VALUE: 1>], Any]], Union[NoneType, Tuple[graia.broadcast.builtin.factory.StatusCodeEnum, graia.broadcast.builtin.factory.ExcInfo]]]`
    :

    `generator_factory: Callable[[Any], AsyncGenerator[Union[NoneType, Tuple[Literal[<ResponseCodeEnum.VALUE: 1>], Any]], Union[NoneType, Tuple[graia.broadcast.builtin.factory.StatusCodeEnum, graia.broadcast.builtin.factory.ExcInfo]]]]`
    :

    `ready: bool`
    :

`DispatcherContextManager(generator_factory: Callable, args=None, kwargs=None)`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

    ### Class variables

    `generator: Generator[Union[NoneType, Tuple[Literal[<ResponseCodeEnum.VALUE: 1>], Any]], Union[NoneType, Tuple[graia.broadcast.builtin.factory.StatusCodeEnum, graia.broadcast.builtin.factory.ExcInfo]], NoneType]`
    :

    `generator_factory: Callable[[Any], Generator[Union[NoneType, Tuple[Literal[<ResponseCodeEnum.VALUE: 1>], Any]], Union[NoneType, Tuple[graia.broadcast.builtin.factory.StatusCodeEnum, graia.broadcast.builtin.factory.ExcInfo]], NoneType]]`
    :

    `ready: bool`
    :

`ExcInfo(exception: Exception, traceback: traceback)`
:   ExcInfo(exception, traceback)

    ### Ancestors (in MRO)

    * builtins.tuple

    ### Instance variables

    `exception: Exception`
    :   Alias for field number 0

    `traceback: traceback`
    :   Alias for field number 1

`ResponseCodeEnum(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Class variables

    `VALUE`
    :

`StatusCodeEnum(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Class variables

    `DISPATCHING`
    :

    `DISPATCH_COMPLETED`
    :

    `DISPATCH_EXCEPTION`
    :

    `EXECUTION_COMPLETED`
    :

    `EXECUTION_EXCEPTION`
    :