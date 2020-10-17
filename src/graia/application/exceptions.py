class InvalidEventTypeDefinition(Exception):
    "不合法的事件类型定义."
    pass

class InvaildAuthkey(Exception):
    "无效的 authKey 或其配置."
    pass

class AccountNotFound(Exception):
    "未能使用所配置的账号激活 sessionKey, 请检查 connect_info 配置."
    pass

class InvaildSession(Exception):
    "无效的 sessionKey, 请重新获取."
    pass

class UnauthorizedSession(Exception):
    "尚未验证/绑定的 session."
    pass

class UnknownTarget(Exception):
    "对象位置未知, 不存在或不可及."
    pass

# FileNotFoundError

# PermissionError

class AccountMuted(Exception):
    "账号在对象所在聊天区域被封禁."
    pass

class TooLongMessage(Exception):
    "消息过长, 尝试分段发送或报告问题."
    pass

class InvaildArgument(Exception):
    "操作参数不合法, 请报告问题."
    pass

class NotSupportedVersion(Exception):
    "该版本不支持本接口."
    pass

class DeprecatedImpl(Exception):
    "该接口已弃用."
    pass

class EntangledSuperposition(Exception):
    "你传入的一个 List[InternalElement] 中包含了一个没有重写 toExternal 的消息元素"
    pass

class MissingNecessaryOne(Exception):
    "应在所提到的参数之中至少传入/使用一个"
    pass

class ConflictItem(Exception):
    "项冲突/其中一项被重复定义"
    pass