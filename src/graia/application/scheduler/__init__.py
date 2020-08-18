# 时间片: 在时间单元内的时间(执行时间为 time_unit.base + time_shape.offset)
# 时间单元: 头尾相接的发生, 但也有例外(mouth是这样的), base是绝对时间
# 时间点: 绝对时间

from pydantic import BaseModel
from datetime import timedelta, datetime
from typing import List, Optional
from abc import abstractmethod, ABC, abstractstaticmethod

class TimeSlice(BaseModel):
    offset: timedelta

class TimeUnit(BaseModel, ABC):
    base: datetime
    children: List[TimeSlice]

    @abstractstaticmethod
    def when() -> Optional[timedelta]:
        """该抽象方法用于描述本时间单位是否开始, 如果不开始预计要在什么时候开始.

        Returns:
            Optional[timedelta]: 若为 `None` 则马上开始, 若不为则在所返回的 timedelta 所定义的时间后开始.
        """

class TimePoint(BaseModel):
    on: datetime