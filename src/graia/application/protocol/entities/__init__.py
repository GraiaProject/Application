from pydantic import BaseModel

class MiraiConfig(BaseModel):
    cacheSize: int
    enableWebsocket: bool