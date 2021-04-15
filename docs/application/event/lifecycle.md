Module graia.application.event.lifecycle
========================================

Classes
-------

`ApplicationLaunched(app)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `app: Any`
    :

`ApplicationLaunchedBlocking(app)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `app: Any`
    :

`ApplicationShutdowned(app)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `app: Any`
    :