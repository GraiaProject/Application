import functools
from typing import Any, Callable, ContextManager, Iterable, List, Union, TypeVar
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

from .exceptions import (
    AccountMuted,
    AccountNotFound,
    InvaildArgument,
    InvaildAuthkey,
    InvaildSession,
    NotSupportedVersion,
    TooLongMessage,
    UnauthorizedSession,
    UnknownTarget,
)
from .context import enter_context
import inspect

_T = TypeVar("_T")


def applicationContextManager(func: Callable):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        with enter_context(app=self):
            return await func(self, *args, **kwargs)

    return wrapper


def requireAuthenticated(func: Callable):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.connect_info.sessionKey:
            raise InvaildSession("you must authenticate before this.")
        return func(self, *args, **kwargs)

    wrapper.__annotations__ = func.__annotations__
    return wrapper


def SinceVersion(*version: int):
    def wrapper(func):
        @functools.wraps(func)
        def inside_wrapper(self, *args, **kwargs):
            if (
                self.connect_info.current_version
                and self.connect_info.current_version < version
            ):
                raise NotSupportedVersion(
                    "the current version does not support this feature: {0}".format(
                        self.connect_info.current_version
                    )
                )
            return func(self, *args, **kwargs)

        return inside_wrapper

    return wrapper


def DeprecatedSince(*version: int, action: str = "warn"):
    if action not in ["warn", "error", "ignore"]:
        raise TypeError("action must be in" + str(["warn", "error", "ignore"]))

    def wrapper(func):
        @functools.wraps(func)
        def inside_wrapper(self, *args, **kwargs):
            if (
                self.connect_info.current_version
                and self.connect_info.current_version > version
            ):
                if action == "error":
                    raise NotSupportedVersion(
                        "the current version deprecated this feature: {0}".format(
                            self.connect_info.current_version
                        )
                    )
                elif action == "warn":
                    import warnings

                    warnings.warn(
                        "'{0}' has been deprecated since {1}, use other methods to realize your business as soon as possible!".format(
                            func.__qualname__, version
                        )
                    )
            return func(*args, **kwargs)

        return inside_wrapper

    return wrapper


code_exceptions_mapping = {
    1: InvaildAuthkey,
    2: AccountNotFound,
    3: InvaildSession,
    4: UnauthorizedSession,
    5: UnknownTarget,
    6: FileNotFoundError,
    10: PermissionError,
    20: AccountMuted,
    30: TooLongMessage,
    400: InvaildArgument,
}


def raise_for_return_code(code: Union[dict, int]):
    if isinstance(code, dict):
        code = code.get("code")
        exception_code = code_exceptions_mapping.get(code)
        if exception_code:
            raise exception_code
    elif isinstance(code, int):
        exception_code = code_exceptions_mapping.get(code)
        if exception_code:
            raise exception_code


def print_traceback_javay():
    stacks = inspect.stack()[1:]
    for i in stacks:
        print(f"    at [{i.filename}:{i.lineno}]")
    print("\n")


class AppMiddlewareAsDispatcher(BaseDispatcher):
    always = True
    context: ContextManager

    def __init__(self, app) -> None:
        self.app = app

    def beforeExecution(self, interface: "DispatcherInterface"):
        self.context = enter_context(self.app, interface.event)
        self.context.__enter__()

    def afterExecution(self, interface: "DispatcherInterface", exception, tb):
        self.context.__exit__(exception.__class__ if exception else None, exception, tb)

    async def catch(self, interface: "DispatcherInterface"):
        from graia.application import GraiaMiraiApplication

        if interface.annotation is GraiaMiraiApplication:
            return self.app


def context_enter_auto(context):
    def wrapper1(func):
        @functools.wraps(func)
        def wrapper2(*args, **kwargs):
            with context:
                return func(*args, **kwargs)

        return wrapper2

    return wrapper1


def call_atonce(*args, **kwargs):
    def wrapper(callable_target):
        return callable_target(*args, **kwargs)

    return wrapper


class InsertGenerator:
    base: Iterable[Any]
    insert_items: List[Any]

    def __init__(self, base_iterable: Iterable, pre_items: List[Any] = None) -> None:
        self.base = base_iterable
        self.insert_items = pre_items or []

    def __iter__(self):
        for i in self.base:
            if self.insert_items:
                yield self.insert_items.pop()
            yield i
        else:
            if self.insert_items:
                yield from self.insert_items[::-1]


class MultiUsageGenerator(InsertGenerator):
    continue_count: int

    def __init__(self, base_iterable: Iterable, pre_items: List[Any] = None) -> None:
        super().__init__(base_iterable, pre_items=pre_items)
        self.continue_count = 0

    def __iter__(self):
        for i in super().__iter__():
            if self.continue_count > 0:
                self.continue_count -= 1
                continue
            yield i


class AutoUnpackTuple:
    def __init__(self, base_iterable: Iterable, pre_items: List[Any] = None) -> None:
        self.base = base_iterable

    def __iter__(self):
        for i in self.base:
            if isinstance(i, tuple):
                yield from i
                continue
            yield i


def yes_or_no(value: bool) -> str:
    return "yes" if value else "no"
