Module graia.application.message.elements
=========================================

Sub-modules
-----------
* graia.application.message.elements.external
* graia.application.message.elements.internal

Functions
---------

    
`isShadowElement(any_instance: Any) ‑> bool`
:   检查实例是否为 Shadow Element
    
    Args:
        any_instance (Any): 欲检查的实例
    
    Returns:
        bool: 是否为 Shadow Element

Classes
-------

`Element(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.message.elements.ExternalElement
    * graia.application.message.elements.InternalElement
    * graia.application.message.elements.ShadowElement

`ExternalElement(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.message.elements.external.FlashImage
    * graia.application.message.elements.external.Image
    * graia.application.message.elements.external.Voice
    * graia.application.message.elements.internal.App
    * graia.application.message.elements.internal.At
    * graia.application.message.elements.internal.AtAll
    * graia.application.message.elements.internal.Face
    * graia.application.message.elements.internal.Json
    * graia.application.message.elements.internal.Plain
    * graia.application.message.elements.internal.Poke
    * graia.application.message.elements.internal.Quote
    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.internal.Source
    * graia.application.message.elements.internal.Voice_LocalFile
    * graia.application.message.elements.internal.Xml

`InternalElement(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation
    * abc.ABC

    ### Descendants

    * graia.application.message.elements.internal.App
    * graia.application.message.elements.internal.At
    * graia.application.message.elements.internal.AtAll
    * graia.application.message.elements.internal.Face
    * graia.application.message.elements.internal.FlashImage
    * graia.application.message.elements.internal.Image
    * graia.application.message.elements.internal.Json
    * graia.application.message.elements.internal.Plain
    * graia.application.message.elements.internal.Poke
    * graia.application.message.elements.internal.Quote
    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.internal.Source
    * graia.application.message.elements.internal.Voice
    * graia.application.message.elements.internal.Voice_LocalFile
    * graia.application.message.elements.internal.Xml

    ### Static methods

    `fromExternal(external_element) ‑> graia.application.message.elements.InternalElement`
    :   可以为异步方法

    ### Methods

    `asDisplay(self) ‑> str`
    :

    `asSerializationString(self) ‑> str`
    :

    `toExternal(self) ‑> graia.application.message.elements.ExternalElement`
    :   可以为异步方法

`ShadowElement(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * graia.application.message.elements.Element
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.message.elements.internal.ShadowImage
    * graia.application.message.elements.internal.Voice_LocalFile