from pydantic import BaseModel, AnyHttpUrl
from typing import Optional, Tuple
import os
import yarl


class Session(BaseModel):
    """用于描述与上游接口会话, 并存储会话状态的实体类.

    Attributes:
        host (AnyHttpUrl): `mirai-api-http` 服务所在的根接口地址
        authKey (str): 在 `mirai-api-http` 配置流程中定义, 需为相同的值以通过安全验证.
        account (int): 应用所使用账号的整数 ID.
        websocket (bool): 是否使用 Websocket 方式获取事件, 若为 `False` 则使用 HTTP 短轮询方式获取事件, 性能较低.
        sessionKey (str, optional): 会话标识, 即会话中用于进行操作的唯一认证凭证, 需要经过 `activeSession` 后才可用.
        current_version (Tuple[int, int, int], optional): 上游服务的版本, 暂时没有自动获取.
    """

    host: AnyHttpUrl
    authKey: str
    account: int
    sessionKey: str = None
    current_version: Tuple[int, int, int] = None
    websocket: bool = True

    @classmethod
    def fromUrl(cls, url: str) -> "Session":
        """不再推荐的声明连接方式的方法, 用于兼容 v3 中的 url 声明连接信息的方法.

        Args:
            url (str): `schema` 为 `mirai` 的链接, 具体请参考 python-mirai(v3) 的文档.

        Returns:
            Session: 从给出的 url 生成的 `Session` 实例.
        """

        yarl_url = yarl.URL(url)
        return cls(
            host=str(
                yarl.URL.build(
                    scheme="http",
                    host=yarl_url.host,
                    port=yarl_url.port,
                )
            ),
            authKey=yarl_url.query["authKey"],
            account=yarl_url.query["qq"],
            websocket=yarl_url.path == "/ws",
        )

    @classmethod
    def fromEnv(
        cls,
        host: Optional[AnyHttpUrl] = None,
        authKey: Optional[str] = None,
        account: Optional[int] = None,
        websocket: Optional[bool] = True,
    ) -> "Session":
        """从环境变量和所给出参数中实例化 Session, 所有参数都必须给出, 无论通过环境变量还是实际给出的值;
        实例化时给出的参数优先级高于环境变量.

        环境变量对应列表:
          - `GRAIA_HOST`: 与参数 `host` 同义;
          - `GRAIA_AUTHKEY`: 与参数 `authKey` 同义;
          - `GRAIA_ACCOUNT_ID`: 与参数 `account` 同义;
          - `GRAIA_WEBSOCKET_ENABLED`: 与参数 `websocket` 同义, 规则:
            - `"true"` 或 `"1"` 得 `True`, 即启用 Websocket 方式连接;
            - `"false"` 或 `"0"` 得 `False`, 即禁用 Websocket 方式连接.

        Args:
            host (AnyHttpUrl, optional): `mirai-api-http` 服务所在的根接口地址
            authKey (str, optional): 在 `mirai-api-http` 配置流程中定义, 需为相同的值以通过安全验证.
            account (int, optional): 应用所使用账号的整数 ID.
            websocket (bool, optional): 是否使用 Websocket 方式获取事件, 若为 `False` 则使用 HTTP 短轮询方式获取事件, 性能较低, 默认为 `True`.

        Returns:
            Session: 从给出的参数和所处环境变量生成的 `Session` 实例.
        """
        return cls(
            **{
                "host": host or os.getenv("GRAIA_HOST"),
                "authKey": authKey or os.getenv("GRAIA_AUTHKEY"),
                "account": account or os.getenv("GRAIA_ACCOUNT_ID"),
                "websocket": websocket
                or ({"false": False, "true": True, "1": True, "0": False}).get(
                    os.getenv("GRAIA_WEBSOCKET_ENABLED").lower(), websocket
                ),
            }
        )

    class Config:
        allow_mutation = True
