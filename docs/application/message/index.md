Module graia.application.message
================================

Sub-modules
-----------
* graia.application.message.chain
* graia.application.message.elements
* graia.application.message.parser

Classes
-------

`BotMessage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `messageId: int`
    :