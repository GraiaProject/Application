"""该模块提供一些便捷的 Timer"""

from datetime import datetime, timedelta
from croniter import croniter

def every(**kwargs):
    while True:
        yield datetime.now() + timedelta(**kwargs)

def every_second():
    """每秒钟执行一次"""
    yield from every(seconds=1)

def every_custom_seconds(seconds: int):
    """每 seconds 秒执行一次

    Args:
        seconds (int): 距离下一次执行的时间间隔, 单位为秒
    """
    yield from every(seconds=seconds)

def every_minute():
    """每分钟执行一次."""
    yield from every(minutes=1)

def every_custom_minutes(minutes: int):
    """每 minutes 分执行一次

    Args:
        minutes (int): 距离下一次执行的时间间隔, 单位为分
    """
    yield from every(minutes=minutes)

def every_hours():
    """每小时执行一次."""
    yield from every(hours=1)

def every_custom_hours(hours: int):
    """每 hours 小时执行一次

    Args:
        hours (int): 距离下一次执行的时间间隔, 单位为小时
    """
    yield from every(hours=hours)

def crontabify(pattern: str):
    """使用类似 crontab 的方式生成计时器

    Args:
        pattern (str): crontab 的设置, 具体请合理使用搜索引擎
    """
    base_datetime = datetime.now()
    crontab_iter = croniter(pattern, base_datetime)
    while True:
        yield crontab_iter.get_next(datetime)