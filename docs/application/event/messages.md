Module graia.application.event.messages
=======================================

Classes
-------

`Forward(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `brief: str`
    :   似乎没有什么用, 这个东西找不到在哪里显示

    `content: List[graia.application.event.messages.ForwardContentMessage]`
    :

    `source: str`
    :   描述, 通常都像: `查看 x 条转发消息` 这样

    `summary: str`
    :

    `title: str`
    :   显示在消息列表中的预览文本, 调用 asDisplay 方法返回该值

    `type: str`
    :   表示该条转发消息的标题, 通常为 `群聊的聊天记录`

    ### Methods

    `asDisplay(self)`
    :

`ForwardContentMessage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `messageChain: graia.application.message.chain.MessageChain`
    :

    `senderId: int`
    :

    `senderName: str`
    :

    `time: datetime.datetime`
    :

`FriendMessage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `messageChain: graia.application.message.chain.MessageChain`
    :

    `sender: graia.application.friend.Friend`
    :

    `type: str`
    :

`GroupMessage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `messageChain: graia.application.message.chain.MessageChain`
    :

    `sender: graia.application.group.Member`
    :

    `type: str`
    :

`SourceElementDispatcher()`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

`TempMessage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.event.MiraiEvent
    * graia.broadcast.entities.event.BaseEvent
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Dispatcher`
    :   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    `messageChain: graia.application.message.chain.MessageChain`
    :

    `sender: graia.application.group.Member`
    :

    `type: str`
    :

    ### Static methods

    `parse_obj(obj)`
    :