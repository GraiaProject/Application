Module graia.application.message.elements.external
==================================================

Classes
-------

`FlashImage(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.external.Image
    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `imageId: Union[str, NoneType]`
    :

    `path: Union[str, NoneType]`
    :

    `type: str`
    :

    `url: Union[str, NoneType]`
    :

    ### Methods

    `asSerializationString(self) ‑> str`
    :

`Image(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.message.elements.external.FlashImage

    ### Class variables

    `imageId: Union[str, NoneType]`
    :

    `path: Union[str, NoneType]`
    :

    `type: str`
    :

    `url: Union[str, NoneType]`
    :

    ### Methods

    `asSerializationString(self) ‑> str`
    :

`Voice(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `path: Union[str, NoneType]`
    :

    `url: Union[str, NoneType]`
    :

    `voiceId: Union[str, NoneType]`
    :

    ### Methods

    `asSerializationString(self) ‑> str`
    :