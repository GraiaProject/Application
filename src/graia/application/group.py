from enum import Enum
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class MemberPerm(Enum):
    "描述群成员在群组中所具备的权限"

    Member = "MEMBER"  # 普通成员
    Administrator = "ADMINISTRATOR"  # 管理员
    Owner = "OWNER"  # 群主


class Group(BaseModel):
    "描述 Tencent QQ 中的可发起聊天区域 '群组(group)' 的能被获取到的信息."

    id: int
    name: str
    accountPerm: MemberPerm = Field(..., alias="permission")


class Member(BaseModel):
    "描述用户在群组中所具备的有关状态, 包括所在群组, 群中昵称, 所具备的权限, 唯一ID."

    id: int
    name: str = Field(..., alias="memberName")
    permission: MemberPerm
    group: Group


class GroupConfig(BaseModel):
    "描述群组各项功能的设置."

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
    "描述群组成员的可修改状态, 修改需要管理员/群主权限."

    name: Optional[str] = None
    specialTitle: Optional[str] = None

    # 调用 json 方法时记得加 exclude_none=True.

    class Config:
        allow_mutation = True
        
class FileList(BaseModel):
    "描述群组文件的有关状态"

    name: Optional[str] = None
    id: Optional[str] = None
    "文件路径"
    path: Optional[str] = None
    "是否为文件"
    is_file: Optional[bool] = None

class FileInfo(BaseModel):
    "群组文件详细信息"

    name: Optional[str] = None
    path: Optional[str] = None
    id: Optional[str] = None
    "文件长度"
    length: Optional[int]
    "下载次数"
    download_times: Optional[int]
    "上传者QQ"
    uploader_id: Optional[int]
    "上传时间"
    upload_time: Optional[int]
    "最后修改时间"
    last_modify_time: Optional[int]
    "文件下载链接"
    download_url: Optional[str] = None
    "文件 sha1 值"
    sha1: Optional[str] = None
    "文件 md5 值"
    md5: Optional[str] = None
