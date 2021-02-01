import abc
from typing import Any, Callable, Optional as O
from pydantic import BaseModel, validator
from graia.application.message.chain import MessageChain
import regex


class NormalMatch(BaseModel, abc.ABC):
    @abc.abstractmethod
    def operator(self) -> str:
        pass


class PatternReceiver(BaseModel):
    name: str
    isGreed: bool = False

    def __init__(self, name: str, isGreed: bool = False) -> None:
        super().__init__(name=name, isGreed=isGreed)

    @validator("name", allow_reuse=True)
    def name_checker(cls, v):
        if not regex.match("^[a-zA-Z_][a-zA-Z0-9_]*$", v):
            raise ValueError("invaild name")
        return v

    def __hash__(self) -> int:
        return super(object, self).__hash__()


class FullMatch(NormalMatch):
    pattern: str

    def __init__(self, pattern) -> None:
        super().__init__(pattern=pattern)

    def operator(self):
        return regex.escape(self.pattern)


class RegexMatch(NormalMatch):
    pattern: str

    def __init__(self, pattern) -> None:
        super().__init__(pattern=pattern)

    def operator(self):
        return self.pattern


class RequireParam(PatternReceiver):
    checker: O[Callable[[MessageChain], bool]] = None
    translator: O[Callable[[MessageChain], Any]] = None


class OptionalParam(PatternReceiver):
    checker: O[Callable[[MessageChain], bool]] = None
    translator: O[Callable[[MessageChain], Any]] = None
