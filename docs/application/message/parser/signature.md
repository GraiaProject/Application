Module graia.application.message.parser.signature
=================================================

Classes
-------

`FullMatch(pattern)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.parser.signature.NormalMatch
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `pattern: str`
    :

    ### Methods

    `operator(self)`
    :

`NormalMatch(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Descendants

    * graia.application.message.parser.signature.FullMatch
    * graia.application.message.parser.signature.RegexMatch

    ### Methods

    `operator(self) ‑> str`
    :

`OptionalParam(name: str, isGreed: bool = False)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.parser.signature.PatternReceiver
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `checker: Union[Callable[[graia.application.message.chain.MessageChain], bool], NoneType]`
    :

    `translator: Union[Callable[[graia.application.message.chain.MessageChain], Any], NoneType]`
    :

`PatternReceiver(name: str, isGreed: bool = False)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.message.parser.signature.OptionalParam
    * graia.application.message.parser.signature.RequireParam

    ### Class variables

    `isGreed: bool`
    :

    `name: str`
    :

    ### Static methods

    `name_checker(v)`
    :

`RegexMatch(pattern)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.parser.signature.NormalMatch
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Class variables

    `pattern: str`
    :

    ### Methods

    `operator(self)`
    :

`RequireParam(name: str, isGreed: bool = False)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.parser.signature.PatternReceiver
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `checker: Union[Callable[[graia.application.message.chain.MessageChain], bool], NoneType]`
    :

    `translator: Union[Callable[[graia.application.message.chain.MessageChain], Any], NoneType]`
    :