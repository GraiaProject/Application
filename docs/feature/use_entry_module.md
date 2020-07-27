# 使用 graia.application.entry 模块

因为我们收到了无数的关于 "为什么 import 这么长" 的报告, 在 Graia Application 0.0.5 版本中,
我们添加了 `graia.application.entry` 模块, 用于为开发者提供快速 import,
以及照顾使用没有 Auto-Import 功能的 IDE 的开发者:

Before:

``` python
from graia.application import GraiaMiraiApplication, Session
from graia.application.protocol.entities.message.chain import MessageChain
from graia.application.protocol.entities.targets.group import Group
```

Now:

``` python
from graia.application.entry import (
    GraiaMiraiApplication,
    Session, MessageChain, Group
)
```