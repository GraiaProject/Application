Module graia.broadcast.builtin.decorators
=========================================

Classes
-------

`Depend(callable, *, cache=False)`
:   

    ### Ancestors (in MRO)

    * graia.broadcast.entities.decorator.Decorator

    ### Class variables

    `cache: bool`
    :

    `depend_callable: graia.broadcast.entities.exectarget.ExecTarget`
    :

    `pre: bool`
    :

    ### Methods

    `target(self, interface: graia.broadcast.interfaces.decorator.DecoratorInterface) ‑> Callable[[Any], Any]`
    :

`OptionalParam(origin: Any)`
:   

    ### Ancestors (in MRO)

    * graia.broadcast.entities.decorator.Decorator

    ### Class variables

    `pre: bool`
    :

    ### Methods

    `target(self, interface: graia.broadcast.interfaces.decorator.DecoratorInterface) ‑> Union[Any, NoneType]`
    :