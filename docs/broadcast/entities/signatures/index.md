Module graia.broadcast.entities.signatures
==========================================

Classes
-------

`Force(content: Any = None)`
:   用于转义在本框架中特殊部分的特殊值
    
    例如：Dispatcher 返回时 None 表示本级 dispatcher 无法满足需求,
    DispatcherInterface 会继续向下查询,
    而某些时候我们确实是需要传递 None 的，
    这时候可以用本标识来保证 None 被顺利作为一个参数传入。
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.signatures.ObjectContainer
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `target: Any`
    :

`ObjectContainer(content: Any = None)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.broadcast.entities.signatures.Force
    * graia.broadcast.entities.signatures.RemoveMe

    ### Class variables

    `target: Any`
    :

`RemoveMe(content: Any = None)`
:   当本标识的实例为一受 Executor 影响的 Listener 返回值时,
    Executor 会尝试在当前 Broadcast 实例中找出并删除本 Listener 实例.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.signatures.ObjectContainer
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `target: Any`
    :