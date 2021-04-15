Module graia.application.event.network
======================================

Classes
-------

`InvaildRequest(**data: Any)`
:   网络异常: 意料之外地, 发出了不被无头客户端接收的 HTTP 请求, 你应该通过相应渠道向我们汇报此问题
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

`RemoteException(**data: Any)`
:   网络异常: 无头客户端处发生错误, 你应该检查其输出的错误日志.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

`SessionRefreshFailed(**data: Any)`
:   网络异常: 检测到无效的 Session 并尝试自动刷新失败.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

`SessionRefreshed(**data: Any)`
:   网络异常: 检测到无效的 Session 并自动刷新, 事件发布时已经刷新成为有效的 Session.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.