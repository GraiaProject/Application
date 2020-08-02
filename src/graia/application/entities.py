from enum import Enum
from pydantic import BaseModel

class UploadMethods(Enum):
    Friend = "friend"
    Group = "group"
    Temp = "temp"

class MiraiConfig(BaseModel):
    cacheSize: int
    enableWebsocket: bool