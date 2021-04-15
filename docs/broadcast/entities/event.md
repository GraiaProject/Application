Module graia.broadcast.entities.event
=====================================

Classes
-------

`BaseEvent(**data: Any)`
:   Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Descendants

    * graia.application.event.MiraiEvent
    * graia.application.event.lifecycle.ApplicationLaunched
    * graia.application.event.lifecycle.ApplicationLaunchedBlocking
    * graia.application.event.lifecycle.ApplicationShutdowned
    * graia.application.event.network.InvaildRequest
    * graia.application.event.network.RemoteException
    * graia.application.event.network.SessionRefreshFailed
    * graia.application.event.network.SessionRefreshed
    * graia.broadcast.builtin.event.ExceptionThrowed
    * graia.broadcast.interfaces.dispatcher.EmptyEvent
    * graia.saya.event.SayaModuleInstalled
    * graia.saya.event.SayaModuleUninstall
    * graia.saya.event.SayaModuleUninstalled

    ### Class variables

    `Config`
    :

`EventMeta(*args, **kwargs)`
:   Metaclass for defining Abstract Base Classes (ABCs).
    
    Use this metaclass to create an ABC.  An ABC can be subclassed
    directly, and then acts as a mix-in class.  You can also register
    unrelated concrete classes (even built-in classes) and unrelated
    ABCs as 'virtual subclasses' -- these and their descendants will
    be considered subclasses of the registering ABC by the built-in
    issubclass() function, but the registering ABC won't show up in
    their MRO (Method Resolution Order) nor will method
    implementations defined by the registering ABC be callable (not
    even via super()).

    ### Ancestors (in MRO)

    * pydantic.main.ModelMetaclass
    * abc.ABCMeta
    * builtins.type