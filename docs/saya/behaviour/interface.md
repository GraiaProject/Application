Module graia.saya.behaviour.interface
=====================================

Classes
-------

`BehaviourInterface(saya_instance: Saya)`
:   

    ### Class variables

    `require_contents: List[graia.saya.behaviour.context.RequireContext]`
    :

    `saya: Saya`
    :

    ### Instance variables

    `currentModule`
    :

    ### Methods

    `allocate_cube(self, cube: graia.saya.cube.Cube) ‑> Any`
    :

    `behaviour_generator(self)`
    :

    `find_route(self, route: str) ‑> Any`
    :

    `require_context(self, module: str, behaviours: List[ForwardRef('Behaviour')] = None)`
    :

    `uninstall_cube(self, cube: graia.saya.cube.Cube) ‑> Any`
    :