Module graia.saya.behaviour.builtin
===================================

Classes
-------

`MountPoint(route_point: str, target: ~T)`
:   Abstract base class for generic types.
    
    A generic type is typically declared by inheriting from
    this class parameterized with one or more type variables.
    For example, a generic mapping type might be defined as::
    
      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
          # Etc.
    
    This class can then be used as follows::
    
      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
          try:
              return mapping[key]
          except KeyError:
              return default

    ### Ancestors (in MRO)

    * graia.saya.behaviour.entity.Router
    * graia.saya.behaviour.entity.Behaviour
    * typing.Generic

    ### Methods

    `route(self, route: str) ‑> ~T`
    :