from typing import Iterable, List, Optional
from datetime import datetime

from graia.application.logger import AbstractLogger, LoggingLogger

Timer = Iterable[datetime]

from asyncio import AbstractEventLoop

from graia.broadcast import Broadcast
from graia.broadcast.entities.decorater import Decorater
from graia.broadcast.entities.dispatcher import BaseDispatcher
from .task import SchedulerTask

class GraiaScheduler:
    loop: AbstractEventLoop
    schedule_tasks: List[SchedulerTask]
    broadcast: Broadcast
    logger: AbstractLogger

    def __init__(self, loop: AbstractEventLoop, broadcast: Broadcast, logger: Optional[AbstractLogger] = None) -> None:
        self.schedule_tasks = []
        self.loop = loop
        self.broadcast = broadcast
        self.logger = logger or LoggingLogger()
    
    def schedule(self, timer: Timer, cancelable: Optional[bool] = False,
        decorators: Optional[List[Decorater]] = None,
        dispatchers: List[BaseDispatcher] = None,
        enableInternalAccess: Optional[bool] = False
    ):
        def wrapper(func):
            task = SchedulerTask(
                func, timer, self.broadcast, self.loop, cancelable,
                dispatchers, decorators, enableInternalAccess, self.logger
            )
            self.schedule_tasks.append(task)
            task.setup_task()
            return func
        return wrapper