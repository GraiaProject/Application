from graia.broadcast import BaseDispatcher
from graia.broadcast.entities.event import BaseEvent
from . import ApplicationDispatcher, EmptyDispatcher


class SessionRefreshed(BaseEvent):
    "网络异常: 检测到无效的 Session 并自动刷新, 事件发布时已经刷新成为有效的 Session."

    Dispatcher = EmptyDispatcher


class SessionRefreshFailed(BaseEvent):
    "网络异常: 检测到无效的 Session 并尝试自动刷新失败."

    Dispatcher = EmptyDispatcher


class RemoteException(BaseEvent):
    "网络异常: 无头客户端处发生错误, 你应该检查其输出的错误日志."

    Dispatcher = EmptyDispatcher


class InvaildRequest(BaseEvent):
    "网络异常: 意料之外地, 发出了不被无头客户端接收的 HTTP 请求, 你应该通过相应渠道向我们汇报此问题"

    Dispatcher = EmptyDispatcher
