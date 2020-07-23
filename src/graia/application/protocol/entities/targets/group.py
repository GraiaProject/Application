from enum import Enum
from pydantic import BaseModel
from pydantic.fields import Field

class MemberPerm(Enum):
    Member = "MEMBER"
    Administrator = "ADMINISTRATOR"
    Owner = "OWNER"

class Group(BaseModel):
    id: int
    name: str
    accountPerm: MemberPerm = Field(..., alias="permission")

class Member(BaseModel):
    id: int
    name: str = Field(..., alias="memberName")
    permission: MemberPerm
    group: Group