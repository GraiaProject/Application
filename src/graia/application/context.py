from contextvars import ContextVar
from contextlib import contextmanager

from graia.application.entities import UploadMethods

application = ContextVar("application")
event = ContextVar("event")
event_loop = ContextVar("event_loop")
broadcast = ContextVar("broadcast")

# for image
# sendGroupMessage 等发送message的指令将set该上下文条目.
image_method = ContextVar("image_method")

@contextmanager
def enter_context(app, event_i):
    t1 = application.set(app)
    t2 = event.set(event_i)
    t3 = event_loop.set(app.broadcast.loop)
    t4 = broadcast.set(app.broadcast)
    yield
    application.reset(t1)
    event.reset(t2)
    event_loop.reset(t3)
    broadcast.reset(t4)

@contextmanager
def enter_message_send_context(method: UploadMethods):
    t = image_method.set(method)
    yield
    image_method.reset(t)