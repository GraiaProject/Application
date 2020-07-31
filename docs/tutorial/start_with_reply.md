# 从一个复读机器人开始...

?> **说明** 从这一章节开始, 我们将使用一些浅显易懂的实例,
来说明 Graia Framework 中的特性和机制, 并利用类比法和更进一步的功能需求作为阶段性的学习案例.

我们先从一个简单的复读机器人开始. 对于我们现在要做的事情, 就是造一个机器人,
使它在收到以 `"复读"` 开头的消息.

我们先给出几个基础知识点:

## 基础知识
从上一章中, 我们了解到 `mirai-api-http` 在与机器人程序建立后, 会给我们的程序发送 "事件",
而我们的程序通过内部的处理, 使我们自己写的业务代码得到运行, 而这些事件中包含了很多非常关键的信息.  

例如第一章中, `FriendMessage` 是我们使用 `bcc.receiver` "订阅" 的事件名称,
而这个名称在程序内部被指向一个同样叫做 `FriendMessage` 的类; 当数据被序列化时,
从 `mirai-api-http` 处传达到的事件就被这个 `FriendMessage` 的类解析, 结果便是一个 `FriendMessage` 实例.

?> **提示** 你可以从模块 `graia.application.protocol.entities.event.messages` 处找到 `FriendMessage` 的定义.

### 获取这个实例
Graia Framework 使用和 `fastapi` 类似的方式, 通过对函数中定义的形式参数进行解析和处理, 得到最后的传参结果;
我们可以通过定义参数的 类型注解(`annotaiton`) 和 默认值(`default`), 在函数体内得到与其相对应或具有对应关系的值.

?> **注意** 部分实现中, 可能定义的参数名也会影响到最后的传参结果

回到问题本身, 我们可以使用这个特性来获取到事件中的 `FriendMessage` 实例:

``` python
from graia.application.protocol.entities.event.messages import FriendMessage

@bcc.receiver("FriendMessage")
async def friend_message_listener(event: FriendMessage):
    # 当事件触发时, 在这个函数体内, event 即是一个 FriendMessage 实例, 也是当前发生的事件的实例.
```

通过 IDE 内置的自动补全功能, 我们可以通过如下的代码得到我们亲爱的消息链:

``` python
from graia.application.protocol.entities.event.messages import FriendMessage

@bcc.receiver("FriendMessage")
async def friend_message_listener(event: FriendMessage):
    print(event.messageChain)
```

但是, 如果就这样下去, 总会有一天写出这样的代码:

``` python
from graia.application.protocol.entities.event.messages import FriendMessage

@bcc.receiver("FriendMessage")
async def friend_message_listener(event: FriendMessage):
    if event.messageChain.asDisplay().startswith("你好!") or\
        event.messageChain.asDisplay().startswith("再见!"):
        if event.messageChain.get(Plain):
            ... # 以下又是一段非常长又非常难看的代码
```

很显然, 这种情况不是我们想看到的, 还记得吗, 我们可以直接通过定义参数部分来获取信息?
是的, 我们可以用这种方式大幅降低代码中 `event.xxxxxxx` 的出现次数:

``` python
from graia.application.protocol.entities.event.messages import FriendMessage
from graia.application.protocol.entities.message.chain import MessageChain

@bcc.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain):
    if message.asDisplay().startswith("你好!") or\
        message.asDisplay().startswith("再见!"):
        if message.get(Plain):
            ...
```

这是不是好多了? 再来扩展一下:

?> **提示** 因为导入的包名实在是太太太长, 所以我们建议你们使用带有自动导入(`Auto Import`)功能的 IDE,
比如 `pycharm`, `VSCode`(加装 `Pylance` 插件), 这也让我们方便了不止一点半点.

``` python
from graia.application.protocol.entities.event.messages import FriendMessage
from graia.application.protocol.entities.message.chain import MessageChain
from graia.application.protocol.entities.targets.friend import Friend

@bcc.receiver("FriendMessage")
async def friend_message_listener(
        message: MessageChain,
        friend: Friend,
        app: GraiaMiraiApplication
    ):
    if message.asDisplay().startswith("你好!") or\
            message.asDisplay().startswith("再见!"):
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain("谢谢, 非常感谢你对我们服务的满意.")
        ]))
```

想想如果不用这项特性, 那么生活将变得多么无趣啊!

?> **注意** 这并不代表使用这项特性就能完全脱离使用类型注解获取事件实例本身, 事实上,
这些也**只不过**是类似于加在一杯咖啡里的几小块方糖, 无论如何, 这仍然*只是*个非常方便的语法糖,
而对于特殊的, 像 `NewFriendRequestEvent`, `MemberJoinRequestEvent` 这样的事件,
你还是需要通过获取事件实例来进行进一步的操作.

<p class="warn"><strong>提示</strong> 如果你对能使用的注解感到迷惑, 可以通过 IDE 的代码跳转 <sup>[1]</sup> 查看事件类的定义, 我们对事件类都标注上了完整的类型注释, 其中的大部分都可以通过这项特性获取到. </p>

于是, 为了尽量写出简单的代码, 你查阅了我们的代码:

``` python
# module: graia.application.protocol.entities.event.messages
...
class GroupMessage(MiraiEvent):
    type: str = "GroupMessage"
    messageChain: MessageChain
    sender: Member

    class Dispatcher(BaseDispatcher):
        mixin = [MessageChainCatcher, ApplicationDispatcher]

        @staticmethod
        def catch(interface: DispatcherInterface):
            if interface.annotation is Group:
                return interface.event.sender.group
            elif interface.annotation is Member:
                return interface.event.sender
...
```

上面的部分非常的直接了当, 但...下面这个 `Dispatcher` 是什么鬼?  

?> **提示** 如果你是个大忙人, 你可以暂时跳过此段, 但我仍然建议你闲下来时读一读这段, 因为本文档不像 v3 的一样,
提供所有事件能用的参数类型注解的说明, 只提供 API Reference,
并且这段为之后我们说明 广播控制(`Broadcast Control`) 机制打下了铺垫.

### 参数解析器(Dispatcher)
当 Graia Framework 解析参数时, 使用的是内部被称为 广播控制(`Broadcast Control`) 的事件系统.

在这个系统中, 解析参数用到了一个或多个的 参数解析器(Dispatcher) 来从当前事件和环境,
也就是 当前上下文(`Current Context`) 中提取相对应的值, 并作为当前参数的解析结果反馈给 执行器(`Executor`),
执行器以此执行了我们的业务代码.

当一个解析器返回 `None` 时, 表示当前解析器无法获取到对应的参数, 通知执行器向下继续启动解析器,
而一旦这之后没有解析器可以启动了, 执行器会抛出 `RequirementCrashed` 错误.

当解析器内定义 `mixin`(混入) 时, 例如上面的代码, 执行器会这样执行:

```
[GroupMessage.Dispatcher -> MessageChainCatcher -> ApplicationDispatcher]
```

而从后两者的名称中, 我们也可以知道我们可以从这个事件中获取到 `MessageChain` 和 `GraiaMiraiApplication` 实例.

于是, 从上述中, 我们了解了 Graia Framework 内部工作机制的一部分, 现在我们已经知道了以下信息:

`GroupMessage` 可以获取到:
 - `MessageChain` 实例 (`GroupMessage.messageChain`)
 - `Group` 实例 (`GroupMessage.sender.group`)
 - `Member` 实例 (`GroupMessage.sender`)
 - `GraiaMiraiApplication` 实例

## 步入实战
很快, 根据上述说明, 我们给出了一段 "可以工作的代码":

[reply_wrong1](/examples/reply_wrong1.py ':include :type=code python')

于是你高高兴兴的启动了应用, 发出 "复读吧!", 期待机器人复读时...

```
Traceback (most recent call last):
  File "...\graia\broadcast\__init__.py", line 121, in Executor
    result = await run_always_await(
  File "...\graia\broadcast\utilles.py", line 15, in run_always_await
    return await any_callable
  File "bot.py", line 30, in group_message_handler
    await app.sendGroupMessage(group, message)
  File "...\graia\application\__init__.py", line 201, in sendGroupMessage
    "messageChain": (await message.build()).dict()['__root__'],
  File "...\graia\application\protocol\entities\message\chain.py", line 77, in build
    raise EntangledSuperposition("You define an object that cannot be sent: {0}".format(i.__class__.__name__))
graia.application.protocol.exceptions.EntangledSuperposition: You define an object that cannot be sent: Source
```

为什么会变成这样呢..... 第一次有了能够自己创造辉煌的能力，又有了像 mirai 和 Graia Framework 这样方便的东西. 两件快乐事情重合在一起.而这两份快乐, 又给我带来更多的快乐. 得到的, 本该是像梦境一般幸福的时间...... 但是, 为什么, 会变成这样呢......

### 安全发送检查器(Sendable Checker)

?> 这项设计是由于 [#90](https://github.com/NatriumLab/python-mirai/issues/90) 和 [这个问题](https://github.com/NatriumLab/python-mirai/issues/64#issuecomment-660088380)

`mirai` 及 `mirai-api-http` 不仅将消息链用于表示 "人眼睛能看到的东西",
还使用 `Source` 和 `Quote` 这两个消息元素(`Message Element`)表示 "作为程序所能解析的一切东西",
而这两个消息元素不能被发送, 同时因为 `sendFriendMessage`, `sendGroupMessage`, `sendTempMessage` 这三个方法中,
消息链的存在感实在是太大, 导致 `quote` 参数顿时变成阿卡林, 从而引发了上面提到的这两个问题.

与此同时, 我们发现有人会有将群图片转发为好友消息, 私聊(临时对话)消息等, 所以我们在安全发送检查器的基础上,
添加了 "图片自动类型转换"(`Image Type Auto Transfer`) 的特性, 使代码更加简洁.

那么, 该如何才能判断一个消息链是否可以被安全发送呢? 我们可以用 `MessageChain.isSendable` 进行检查:

``` python
@bcc.receiver("GroupMessage")
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith("复读"):
        print(message.isSendable) # -> False
        await app.sendGroupMessage(group, message)
```

运行以上代码, 我们发现默认情况下, 从参数解析器中获取到的消息链不可以被安全发送,
所以我们需要使用 `MessageChain.asSendable` 方法将消息链转换为可以被安全发送的形式:

``` python
@bcc.receiver("GroupMessage")
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    if message.asDisplay().startswith("复读"):
        await app.sendGroupMessage(group, message.asSendable())
```

再试试, 你会发现复读机成功的运作起来了!

<div class="panel-view">
  <div class="controls">
    <div class="circle red"></div>
    <div class="circle yellow"></div>
    <div class="circle green"></div>
    <div class="title">好友聊天</div>
  </div>
  <div class="content">
    <div class="chat-message shown">
      <div class="avatar" style="background-color: rgb(204, 0, 102); ">A</div>
      <div class="nickname">Alice</div>
      <div class="message-box">复读 复读机可以用了!</div>
    </div>
    <div class="chat-message shown">
      <div class="avatar" style="background-color: rgb(11, 135, 218); ">B</div>
      <div class="nickname">Bot</div>
      <div class="message-box">复读 复读机可以用了!</div>
    </div>
  </div>
</div>

以下是复读机完整, 可正常运行的代码:

[reply_right](/examples/reply_right.py ':include :type=code python')


[1] VSCode 内通常使用 `Alt + 鼠标左键单击`, 而 Pycharm 默认为 `Ctrl + 鼠标左键单击`
