from pydantic import BaseModel

class Friend(BaseModel):
    id: int
    nickname: str
    remark: str