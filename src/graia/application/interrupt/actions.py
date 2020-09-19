import abc
from typing import Any

class Action(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def executer(self) -> Any: ...