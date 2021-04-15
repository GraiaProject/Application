Module graia.saya.event
=======================

Classes
-------

`SayaModuleInstalled(**data: Any)`
:   不用返回 RemoveMe, 因为 Cube 在被 uninstall 时会被清理掉, 如果你用的是规范的 Saya Protocol 的话.
        
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `channel: graia.saya.channel.Channel`
    :

    `module: str`
    :

`SayaModuleUninstall(**data: Any)`
:   不用返回 RemoveMe, 因为 Cube 在被 uninstall 时会被清理掉, 如果你用的是规范的 Saya Protocol 的话.
        
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `channel: graia.saya.channel.Channel`
    :

    `module: str`
    :

`SayaModuleUninstalled(**data: Any)`
:   不用返回 RemoveMe, 因为 Cube 在被 uninstall 时会被清理掉, 如果你用的是规范的 Saya Protocol 的话.
        
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `module: str`
    :