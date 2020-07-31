# 监听事件与传播控制

在前几章的说明中, 我们基本上将监听器的函数体部分介绍完毕了,
而监听器的主要用途则是用于监听事件, 向执行器提供用于参数解析的参数,
并在这个过程中可以控制执行链(即 `Execution Chain`)上的事件传播.

## 基本的事件监听
在广播控制中, 监听器的注册是通过 `Broadcast.receiver` 方法完成的:

``` python
@bcc.receiver("GroupMessage")
def im_listener():
    pass
```

如上, 我们使用 `Broadcast.receiver` 注册了函数 `im_listener` 为事件 `GroupMessage` 的监听器,
而这段代码等同于:

``` python
from graia.application.entry import GroupMessage

@bcc.receiver(GroupMessage)
def im_listener():
    pass
```

在这里, `GroupMessage` 才是真正的事件类, 而之前使用字符串的监听注册则是我们提供的一个语法糖,
在此我们推荐使用后一种方式.

## 事件的传播过程

当 `mirai-api-http` 通过 Websocket 或者短轮询的方式向我们的程序内部传递事件时,
内置的事件接收器会在序列化数据后, 将得到的事件对象通过 `Broadcast.postEvent` 启动 `Broadcast.layered_scheduler`,
即 "分层事务发生器". `Broadcast.layered_scheduler` 将不同执行优先级的监听器分层,
并按优先级 **从最小的到最大的** 进行并发, 这意味着只要你的监听器的优先级越小, 它就执行的越早.

你可以在调用 `Broadcast.receiver` 时手动指定优先级(`priority`):

``` python
@bcc.receiver(GroupMessage, priority=8)
```

?> **提示** 我们在包 `graia.broadcast.priority` 下设置了一个枚举类,
它的名字是 `Priority`, 如果有手动设置优先级的需要, 请尽量使用本枚举类声明.

当监听器内部发生错误时(不限于函数体, 包括 `Dispatcher`, `Decorater` 等),
如果是一般错误, 则广播控制系统会广播 `ExceptionThrowed` 事件;
但如果是 `PropagationCancelled`(传播终止), 则广播控制系统会在执行完本优先级层上的所有监听器后不再去执行下一层.

!> **警告** 如果你将所有的监听器的优先级都设做同一个值(如默认值 `16`),
则你的 `PropagationCancelled` 是无效的.

## 参数解析(Dispatch)和参数装饰(Decorate)

上一节中, `Broadcast.postEvent` 启动了 `Broadcast.layered_scheduler`,
同时, 我们了解了 `Broadcast.layered_scheduler` 是如何控制事件的传播的.
那么这节中, 我们将了解当执行器被执行时, 广播控制是如何解析函数体中的参数的.


### 参数解析器(Dispatcher) 和 解析器接口(Dispatcher Interface)
`Broadcast.layered_scheduler` 对监听器进行分层, 并对每一层都进行并发(`asyncio.wait`).
在并发前, 它会先用 `ExecutorProtocol` 包装监听器等环境变量, 再传入 `Broadcast.Executor`,
由它来执行对参数的解析和装饰, 并将解析后得到的参数传入函数体执行我们的业务代码.

在 `Broadcast.Executor` 中, `Dispatcher` 是参数解析中的重要成员,
它们通过分析当前上下文, 向外抛出值(`return` 或者是 `yield`),
从而使 `Broadcast.Executor` 得到向函数体传入的值.
`DispatcherInterface` 是调控 `Dispatcher` 的重要单位,
它通过 python 中提供的 上下文管理器(`Context manager`) 特性,
全自动的将当前上下文准确无误的传递给 `Dispatcher`, 并通过他们的输出判断是否继续向下查询(lookup).

如果 `DispatcherInterface` 在提供给它的所有 `Dispatcher` 中都无法查询到可以作为返回值的结果,
会向上抛出 `RequirementCrashed` 错误.

### 参数修饰器(Decorater) 和 修饰器接口(Decorater Interface)

?> 关于 `Decorater` 应为 `Decorator`: 这里是一个笔误, 但无伤大雅.

`Decorater` 被用于对 `Dispatcher` 返回的 "抛出值" 加以修饰.  
`DecoraterInterface` 实为一个内置的 `Dispatcher`, 但 `Broadcast.Executor` 将保证它会被第一个运行.

`DecoraterInterface` 在定位上类似 `Dispatcher` 之于 `DispatcherInterface`,
由它来对 `Decorater` 进行执行并捕获抛出值;
但不同的是, `DecoraterInterface` 允许拥有状态(`DecoraterInterface.local_storage`).