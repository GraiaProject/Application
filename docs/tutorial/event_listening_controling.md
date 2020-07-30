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
如果是一般错误, 则广播控制系统会