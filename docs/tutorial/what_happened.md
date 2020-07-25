# 发生了什么?!

在上一章中, 我们与机器人发生了一次简单的对话, 接下来我们将说明这一切的背后究竟发生了什么.

?> **提示** 如果你曾使用过 `python-mirai`(v3), 你或许和 nonebot 中描述的 "已经有较丰富的 QQ 机器人开发经验，尤其是使用 CQHTTP 插件的经验" 的人是相似的, 但 `Graia Framework` 是重新根据 `nonebot`, `python-mirai`, 甚至与机器人框架无关的多种 web 后端开发框架, 例如 `fastapi`, `flask` 等框架的弱点和优点, 以及 `mirai` 这个机器人平台所具备的优势和不同所思考, 设计的, 一切都大不相同了.

## 从 mirai 开始
接触了这个项目的你肯定知道, `mirai` 是一款 QQ 的协议库和机器人框架, 所以我们先从这里开始.

?> 和 `CoolQ(酷Q)` 一样, `mirai` 同样也是个机器人开发平台, 但 `mirai` 通常指代整个 `Project Mirai`,
其核心部分 `mirai-core` 实现了与 QQ 服务器的交互, 而其外围部分, 即 `mirai-console` 和 `mirai-api-http`,
则是用于与其他程序进行交互, 这些项目共同组成了整个机器人开发平台.

我们的程序通过 `Graia Framework` 的协议实现部分, 与 `mirai-api-http` 进行通信, 并获取到从 QQ 服务器传输来的事件:

![image](/assets/images/process_1.png)

然后, `mirai-api-http` 从 `mirai` 获取到了事件, 并分发给我们的程序, 于是从 `mirai` 到 `Graia Framework` 的过程便告一段落.

## 广播控制(Broadcast Control)
事件(`Event`) 到达了我们的程序, 接下来, 我们的数据解析器开始工作, 不过这个部分目前你可以忽略;
数据解析完后, 作为事件的部分就被运输到内部称为 广播控制(`Broadcast Control`) 的部分.

?> **Tip** 如果你这之前有接触过类似 `EventBus`, `blinker` 这样的 "事件处理系统",
你可以将广播控制看作他们的升级版本, 其中的不同我们之后会再阐述.

你会发现, 我们调用的 `app` 并不是外部的 `GraiaMiraiApplication` 实例, 而是被定义于函数头的一个形参:

``` python
...
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    ...
```

那么, 为什么它在被执行时正常工作? 这里我们就需要牵扯到 广播控制(`Broadcast Control`).

当事件被解析好, 运输到广播控制时, 我们的处理器会调用类实例 `Broadcast` 的方法: `Broadcast.postEvent`;
这个方法用于在程序内部 "广播" 事件, 接收到广播的函数, 我们称它们为 监听者(`Listener`).

监听者收到了来自某个地方的事件, 便检查它是否有义务去执行它, 如果有, 则进入下一个阶段:  
我们以它定义的 参数标记(`Signature`), 根据事件类所定义的 参数解析器(`Dispatcher`) 对其进行分析,
以此得出最后需要传入的参数, 并执行监听者, 然后我们便进入了下一个阶段.

## 落叶归根
从土里来的叶子, 终究是要回到土里去的.
虽然在某种程度上, 这个比喻并不贴切, 但用在这里还是很形象的.

监听者执行, 它执行的正是我们的代码, 我们在这个例子里简单的调用了 `GraiaMiraiApplication.sendFriendMessage` 方法,
通过这种方式发出了一条好友消息来回应我们的消息, 而在简单的调用过程中, 却发生了非常多的事情:

 - 你通过直接构建 `MessageChain` 获得了一个 "消息链" 实例, 并将其传入
 - 方法接收到了你的请求, 检查了你的消息链以确保可以被安全的发送, 并通过 `MessageChain.build` 方法得到了一个可以被直接发送的消息链实例.
 - 消息链实例与你提供的其他信息, 被发往 `mirai-api-http`, `mirai-api-http` 验证完了请求有效性, 忠实的完成了任务, 并返回了一个 `BotMessage` 实例.

`BotMessage` 实例可以被用于撤回我们账号发出的消息, 这可能是这个实例唯一的用途.

至此, 我们已经知道了这次对话中到底都发生了些什么, 以及 `Graia Framework` 如何广播事件并调用到相应的监听者来运行事务代码. 接下来的文档中我们将一步步使用 `Graia Framework` 的各项特性对我们的程序进行扩充, 以实现更加强大的功能.