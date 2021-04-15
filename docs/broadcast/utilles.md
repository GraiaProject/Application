Module graia.broadcast.utilles
==============================

Variables
---------

    
`T`
:   class NestableIterable(Iterable[T]):
        index_stack: list
        iterable: Iterable[T]
    
        def __init__(self, iterable: Iterable[T]) -> None:
            self.iterable = iterable
            self.index_stack = [0]
    
        def __iter__(self):
            index = self.index_stack[-1]
            self.index_stack.append(self.index_stack[-1])
    
            start_offset = index + int(bool(index))
            try:
                for self.index_stack[-1], content in enumerate(
                    itertools.islice(self.iterable, start_offset, None, None),
                    start=start_offset,
                ):
                    yield content
            finally:
                self.index_stack.pop()
    
        def with_new(self, target):
            self.iterable = target
            return self

Functions
---------

    
`argument_signature(callable_target)`
:   

    
`dispatcher_mixin_handler(dispatcher: graia.broadcast.entities.dispatcher.BaseDispatcher) ‑> List[graia.broadcast.entities.dispatcher.BaseDispatcher]`
:   

    
`flat_yield_from(l)`
:   

    
`group_dict(iw: iterwrapper.wrapper.IterWrapper, key: Callable[[Any], Any])`
:   

    
`is_asyncgener(o)`
:   

    
`isasyncgen(o)`
:   

    
`iscoroutinefunction(o)`
:   

    
`printer(value)`
:   

    
`run_always_await(any_callable)`
:   

    
`run_always_await_safely(callable, *args, **kwargs)`
:   

Classes
-------

`NestableIterable(iterable: Iterable[~T], generator_with_index_factory: Callable[[Iterable[~T], ~I], Generator[NoneType, NoneType, Tuple[~I, ~T]]] = None, index_increase_func: Callable[[~I, Iterable[~T]], ~I] = <function NestableIterable.<lambda>>, initial_index_value_factory: Callable[[], ~I] = <function NestableIterable.<lambda>>, is_index_origin: Callable[[~I], bool] = <function NestableIterable.<lambda>>)`
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

    * typing.Generic

    ### Class variables

    `generator_with_index_factory: Callable[[Iterable[~T], ~I], Generator[NoneType, NoneType, Tuple[~I, ~T]]]`
    :

    `index_increase_func: Callable[[~I, Iterable[~T]], ~I]`
    :

    `indexes: List[~I]`
    :

    `is_index_origin: Callable[[~I], bool]`
    :

    `iterable: Iterable[~T]`
    :

    ### Static methods

    `default_generator_factory(iterable: Iterable[~T], start: ~I)`
    :

`as_sliceable(iterable)`
: