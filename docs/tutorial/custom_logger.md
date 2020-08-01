# 自定义 Logger

有些时候, 你需要将一个机器人机制并入一个已有的系统,
但苦于其不能和现有的机制合用, 比如说日志.

`graia-application` 提供了一个极简抽象的 `AbstractLogger` 作为内置的对不同日志系统的抽象封装,
并实现了基于标准库的 `logging` 的 `LoggingLogger`, 以作为默认使用的日志库.

当然, 你也可以通过继承 `AbstractLogger`, 并实现其要求实现的抽象方法,
通过在实例化 `GraiaMiraiApplication` 时传参 `logger` 为你的实现的类实例:

``` python
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=...,
    logger=CustomLogger()
)
```