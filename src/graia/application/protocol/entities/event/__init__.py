from pydantic import BaseModel, validator
from graia.broadcast import BaseEvent
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.application.protocol.entities.targets.group import Member, Group
from graia.application.protocol.exceptions import (
    InvalidEventTypeDefinition)
class MiraiEvent(BaseEvent, BaseModel):
    __base_event__ = True
    type: str

    @validator("type")
    def type_limit(cls, v):
        if cls.type != v:
            raise InvalidEventTypeDefinition("{0}'s type must be '{1}', not '{2}'".format(cls.__name__, cls.type, v))
        return v

    class Config:
        extra = "forbid"

    class Dispatcher:
        pass