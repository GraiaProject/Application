from typing import Callable
from . import TimePoint, TimeSlice, TimeUnit
from datetime import datetime, timedelta
import asyncio

class DayUnit(TimeUnit):
    @staticmethod
    def when():
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(minute=0, hour=0, second=0, microsecond=0)
        return tomorrow - now

class HourUnit(TimeUnit):
    @staticmethod
    def when():
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return next_hour - now

class MinuteUnit(TimeUnit):
    @staticmethod
    def when():
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        return next_minute - now

class SecondSlice(TimeSlice):
    offset: timedelta = timedelta(seconds=1)

class MinuteSlice(TimeSlice):
    offset: timedelta = timedelta(minutes=1)

class HourSlice(TimeSlice):
    offset: timedelta = timedelta(hours=1)

class DaySlice(TimeSlice):
    offset: timedelta = timedelta(days=1)

class MonthSlice(TimeSlice):
    @property
    def offset(self) -> timedelta:
        now_month = datetime.now().month
        if now_month in (1, 3, 5, 7, 8, 10, 12):
            return timedelta(days=30)
        else:
            return timedelta(days=31)

class SchedulerControl:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
    
    def schedule_callable(self, callable: Callable, unit: TimeUnit, *args, **kwargs) -> asyncio.Task:
        """使用 asyncio 提供的各式 API, 将给出的 Callable 对象作为调度对象, 并根据所给出的时间单位作出决策.

        Args:
            callable (Callable): 任意调度对象
            unit (TimeUnit): 时间单位

        Returns:
            asyncio.Task: undefined.
        """
        pass