from enum import Enum
from typing import Optional
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

class GroupConfig(BaseModel):
    name: Optional[str] = None
    announcement: Optional[str] = None
    confessTalk: Optional[bool] = None
    allowMemberInvite: Optional[bool] = None
    autoApprove: Optional[bool] = None
    anonymousChat: Optional[bool] = None

    # 调用 json 方法时记得加 exclude_none=True.

    class Config:
        allow_mutation = True

class MemberInfo(BaseModel):
    name: Optional[str] = None
    specialTitle: Optional[str] = None

    # 调用 json 方法时记得加 exclude_none=True.

    class Config:
        allow_mutation = True