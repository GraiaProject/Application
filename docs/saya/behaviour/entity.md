Module graia.saya.behaviour.entity
==================================

Classes
-------

`Behaviour()`
:   

    ### Descendants

    * graia.saya.behaviour.entity.Router
    * graia.saya.builtins.broadcast.behaviour.BroadcastBehaviour

    ### Methods

    `allocate(self, cube: graia.saya.cube.Cube[typing.Any]) ‑> Any`
    :

    `route(self, route: str) ‑> Any`
    :

    `uninstall(self, cube: graia.saya.cube.Cube[typing.Any]) ‑> Any`
    :

`Router()`
:   

    ### Ancestors (in MRO)

    * graia.saya.behaviour.entity.Behaviour

    ### Descendants

    * graia.saya.behaviour.builtin.MountPoint

    ### Methods

    `allocate(self, cube: Any) ‑> Any`
    :

    `route(self, route: str) ‑> Any`
    :

    `uninstall(self, cube: graia.saya.cube.Cube[typing.Any]) ‑> Any`
    :