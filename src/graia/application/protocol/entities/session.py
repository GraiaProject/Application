from pydantic import BaseModel, AnyHttpUrl
from typing import Tuple
import yarl

class Session(BaseModel):
    host: AnyHttpUrl
    authKey: str
    account: int
    sessionKey: str = None
    current_version: Tuple[int, int, int] = None
    websocket: bool = True

    @classmethod
    def fromUrl(cls, url: str) -> "Session":
        yarl_url = yarl.URL(url)
        return cls(
            host=str(yarl.URL.build(
                scheme="http",
                host=yarl_url.host,
                port=yarl_url.port,
            )),
            authKey=yarl_url.query["authKey"],
            account=yarl_url.query["qq"],
            websocket=yarl_url.path == "/ws"
        )

    class Config:
        allow_mutation = True