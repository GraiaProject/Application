# 编码建议: 不要自造 Handler

?> 事出有因: [#9](https://github.com/GraiaProject/Application/issues/9) 等

在处理对于事件系统的问题时, 我们发现了一个非常非常尴尬的事实:
开发者都喜欢自己造一个消息处理器, 并且在我们提供的事件系统上只实现了一个 Listener 用于对接自己的处理器.  

这是非常愚蠢的, 我们不妨来看看, 这些错误的示例:

 - 使用一个类似 `MyHandler.commands` 的列表/字典, 存储的大多是自己真正的业务部分,
 而在我们提供的事件系统上只挂了一个孤零零的监听器.
 - 直接调用了 `GraiaMiraiApplication.fetch_message` 方法,
 将生成的事件实例直接投入自己的应用内部处理, 并且大多数还又包装了一层.

哦, 我的老天爷, 我真想用你亨利叔叔那肮脏的靴子狠狠的踢你的屁股!

## 动机何在?
我们对其进行了一定程度上的分析, 发现这些实现的开发者大多都有这样的需求:

 - 对消息进行过滤, 认为普通的 Listener 如果需要实现这样的过滤只能 copy&paste, 不好;
 - 需要分析消息后将分析结果传入自己的业务代码处理, 而这里又以为要 copy&paste, 不好;
 - 对消息事件本身进行封装.

我们将对这些需求进行一步步的刨析, 并给出我们建议的解决方案.

## 基础知识

?> **提示** 如果你还没看过 [内部运作流程](tutorial/event_listening_controling "Graia Framework - 内部运作流程"),
和特性一节, 还不赶紧去看!

在之前的文档中, 我们说过, 内置的事件系统 "广播控制"(`Broadcast Control`, 简称 `BCC`),
使用了非常巧妙的设计完成了以下三个大点:

 - 监听器传入参数解析(`Dispatcher`)
 - 事件的传递干涉(`layered_scheduler`)
 - 用户层面对传入参数的扩展(`Decorater`)

而今天我们就使用这些特性来完成上面所说到的这三点.

## 过滤消息

我们的需求非常非常的简单: 检测消息, 如果不符合要求就停止执行.
这里我们可以使用来自 BCC 的特性: 无头参数修饰器(`Headless Decorater`).

不知你们是否还记得, v3时, 我们提供了一个 `Depend` 作为依赖注入的支持,
这个设计来自 `fastapi`. 如果是从来没用过的用户, 你就只要知道 `Depend` 会在函数体被执行之前执行就好了,
而它是和函数体一样, 都可以使用 `Dispatcher`, `Decorater`, 甚至完整的参数解析,
且它在 `Graia Framework` 中, 是一个 `Decorater` 实现, 可以用无头参数修饰器这个特性.

在 BCC 的 `0.0.6` 版本中, 提供了一个非常非常有趣的玩意: `ExecutionStop`,
这是一个错误类, 于是你需要使用 `raise` 关键字来使用它.
但它主要用于在业务代码或是解析阶段结束当前的执行, 并返回空值给上一层.
这里我们只需要知道在这里我们需要用到它就是了.

假设你已经有了个判断消息链是否有效的函数:

``` python
def judge(message: MessageChain) -> bool:
    ...
```

于是, 我们就可以利用这个函数做一个 `Depend` 内需要使用的函数:

``` python
def judge_depend_target(message: MessageChain):
    if not judge(message):
        raise ExecutionStop()
```

我们可以在调用 `Broadcast.receiver` 时, 提供 `headless_decoraters` 参数,
通过无头参数修饰器来使用我们上面的这个判断函数:

``` python
@bcc.receiver("GroupMessage", headless_decoraters=[
    Depend(judge_depend_target)
])
async def ...():
    ...
```

不出意外, 这个监听器只会在函数 `judge` 返回 `True` 时被执行.