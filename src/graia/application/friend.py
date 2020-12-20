from pydantic import BaseModel


class Friend(BaseModel):
    "描述 Tencent QQ 中的可发起对话对象 '好友(friend)' 的能被获取到的信息."

    id: int
    nickname: str
    remark: str
