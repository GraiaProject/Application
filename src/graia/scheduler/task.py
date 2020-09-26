import traceback
from typing import Any, Callable, Coroutine, Generator, List, Optional, Tuple, Type, Union
import asyncio
from graia.broadcast.entities.decorater import Decorater
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.listener import Listener
from graia.application.logger import AbstractLogger, LoggingLogger
from graia.scheduler.exception import AlreadyStarted

from graia.scheduler.utilles import EnteredRecord, print_track_async
from .event import SchedulerTaskExecute
from graia.broadcast import Broadcast
from datetime import datetime
from . import Timer

class SchedulerTask:
    target: Callable[..., Any]
    timer: Timer
    task: asyncio.Task

    broadcast: Broadcast
    dispatchers: List[Union[
        Type[BaseDispatcher],
        Callable,
        BaseDispatcher
    ]]
    decorators: List[Decorater]
    enableInternalAccess: bool = False

    cancelable: bool = False
    stoped: bool = False

    sleep_record: EnteredRecord
    started_record: EnteredRecord

    loop: asyncio.AbstractEventLoop
    _logger: AbstractLogger

    @property
    def is_sleeping(self) -> bool:
        return self.sleep_record.entered
    
    @property
    def is_executing(self) -> bool:
        return not self.sleep_record.entered
    
    def __init__(self,
        target: Callable[..., Any],
        timer: Timer,
        broadcast: Broadcast,
        loop: asyncio.AbstractEventLoop,
        cancelable: bool = False,
        dispatchers: Optional[List[Union[
            Type[BaseDispatcher],
            Callable,
            BaseDispatcher
        ]]] = None,
        decorators: Optional[List[Decorater]] = None,
        enableInternalAccess: bool = False,
        logger: Optional[AbstractLogger] = None
    ) -> None:
        self.target = target
        self.timer = timer
        self.broadcast = broadcast
        self.loop = loop
        self.cancelable = cancelable
        self.dispatchers = dispatchers or []
        self.decorators = decorators or []
        self.enableInternalAccess = enableInternalAccess
        self.sleep_record = EnteredRecord()
        self.started_record = EnteredRecord()
        self._logger = logger or LoggingLogger()

    def setup_task(self) -> None:
        if not self.started_record.entered: # 还未启动
            self.task = self.loop.create_task(self.run())
        else:
            raise AlreadyStarted("the scheduler task has been started!")

    def sleep_interval_generator(self) -> Generator[float, None, None]:
        for next_execute_time in self.timer:
            if self.stoped:
                return
            now = datetime.now()
            if next_execute_time >= now:
                yield (next_execute_time - now).total_seconds()
    
    def coroutine_generator(self) -> Generator[Tuple[Coroutine, bool, Optional[float]], None, None]:
        for sleep_interval in self.sleep_interval_generator():
            yield (asyncio.sleep(sleep_interval), True, sleep_interval)
            yield (self.broadcast.Executor(
                target=Listener(
                    callable=self.target,
                    namespace=self.broadcast.getDefaultNamespace(),
                    inline_dispatchers=self.dispatchers,
                    priority=16,
                    listening_events=[SchedulerTaskExecute],
                    headless_decoraters=self.decorators,
                    enableInternalAccess=self.enableInternalAccess
                ),
                event=SchedulerTaskExecute()
            ), False, None)
    
    @print_track_async
    async def run(self) -> None:
        for coro, waiting, sleep_interval in self.coroutine_generator():
            if waiting: # 是否为 asyncio.sleep 的 coro
                with self.sleep_record:
                    try:
                        await coro
                    except asyncio.CancelledError:
                        return
            else: # 执行
                if self.cancelable:
                    try:
                        await coro
                    except asyncio.CancelledError:
                        if self.cancelable:
                            return
                        raise
                    except Exception as e:
                        self._logger.error(
                            "an unexcepted exception ({0}) raised by a scheduler task, it's {1}".format(
                                e.__class__.__name__, self.target
                        ))
                        traceback.print_exc()
                else:
                    try:
                        await asyncio.shield(coro)
                    except asyncio.CancelledError:
                        self._logger.debug("a scheduler task has been cancelled: {}".format(self.target))
                    except Exception as e:
                        self._logger.error(
                            "an unexcepted exception ({0}) raised by a scheduler task, it's {1}".format(
                                e.__class__.__name__, self.target
                        ))
                        traceback.print_exc()

    def stop_interval_gen(self) -> None:
        if not self.stoped:
            self.stoped = True
    
    async def join(self, stop=False):
        if stop and not self.stoped:
            self.stop_interval_gen()
        
        if self.task:
            await self.task
    
    def stop(self):
        if not self.task.cancelled():
            self.task.cancel()