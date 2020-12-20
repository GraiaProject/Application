from enum import Enum
from pydantic import BaseModel


class UploadMethods(Enum):
    """用于向 `uploadImage` 或 `uploadVoice` 方法描述图片的上传类型"""

    Friend = "friend"
    Group = "group"
    Temp = "temp"


class MiraiConfig(BaseModel):
    """`/config` 接口的序列化实体类"""

    cacheSize: int
    enableWebsocket: bool
