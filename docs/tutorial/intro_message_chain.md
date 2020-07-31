# 消息链(Message Chain)和消息元素(Message Element)

消息链(`Message Chain`) 被用于容纳各式 消息元素(`Message Element`),
借此描述所有发生在聊天过程中被发出或是接收到的消息.

## 消息元素
消息元素是消息链的基本组成部分, 分为内部态(`Internal Element`)和外部态(`External Elenet`);  

简单的说明:

 - 内部态主要用于向开发者提供抽象程度更高的用户接口, 提供 `fromExternal` 和 `toExternal` 方法来进行态素转换.
 - 外部态主要用于与无头客户端的通讯; 序列化和反序列化都是由外部态完成.

我们在 `Graia Application for Mirai` 中, 提供了多种消息元素,
你可以在包 `graia.application.protocol.entities.message.elements.internal` 处寻找到各式元素定义.

## 消息链
消息链由单数个或复数个的消息元素组成, 有以下属性:

 - 可变(`Mutable`) 和 不可变(`Immutable`);
 - 是否可发送(`Sendable`)

可变与不可变表现在 `MessageChain.__root__` 的类型上: 如果是 `tuple` 类型, 则不可变; 这也是 `parse_obj` 和 `build` 方法的默认返回形式.

可发送表现在 `MessageChain.__root__` 的各个元素的 `toExternal` 方法是否有效:
 - 如果为外部态且内部态类中 `toExternal` 定义不合法: 该元素不可发送 -> 该消息链不可发送
 - 如果定义指向 `InternalElement.toExternal`: 该元素不可发送 -> 该消息链不可发送

### 消息链中的各式方法

#### MessageChain.create

(classmethod) MessageChain.**create**(*elements*: `Sequence[InternalElement | ExternalElement]`)
 - 返回值类型: `MessageChain`
 - 描述: 根据提供的序列(列表或者元组), 创建消息链.

#### MessageChain.get

(method) MessageChain.**get**(*element_class*: `Type[InternalElement] | Type[ExternalElement]`)
 - 返回值类型: `List[Type[InternalElement] | Type[ExternalElement]]`
 - 描述: 提供特定的消息元素类型, 返回消息链中 **所有** 的同类型元素.

1. 你可以获取从消息链中获取一种特定的所有元素:

``` python
message.get(Plain)
```

2. 你可以获取从消息链中获取多种特定的所有元素:

``` python
message.get((Plain, At, AtAll))
```

3. 因为结果可能是个空列表, 你可以以此判断消息中是否包含特定元素:

``` python
attempt_fetch = message.get(Image)
if not attempt_fetch:
    await app.sendGroupMessage(group, MessageChain.create([
        Plain("你需要在消息中包含至少一张图片!")
    ]))
```

4. 你也可以这样代替本方法的调用:

``` python
attempt_fetch = message[Image]

message[Image, Plain]
```

#### MessageChain.has

(method) MessageChain.**has**(*element_class*: `Type[InternalElement] | Type[ExternalElement]`)
 - 返回值类型: `bool`
 - 描述: 提供特定的消息元素类型, 查询消息链中是否有匹配的元素, 如果有就返回 `True`, 若无则是 `False`.

1. 你可以以此判断消息中是否包含特定元素:

``` python
if not message.has(Image):
    await app.sendGroupMessage(group, MessageChain.create([
        Plain("你需要在消息中包含至少一张图片!")
    ]))
```

2. 你可以同时检查是否含有多种的元素, 这些参数是 `或` 关系的:

``` python
message.has((Plain, Image))
```

#### MessageChain.join

(classmethod) MessageChain.**join**(**chains*: `MessageChain`)
 - 返回值类型: `MessageChain`
 - 描述: 拼接所提供的所有消息链, 并返回一个新的消息链作为拼接的结果.

!> 本方法实现有误, 等之后版本撤出这条警告再用.

#### MessageChain.plus

(method) MessageChain.**plus**(**chains*: `MessageChain`)
 - 返回值类型: `NoReturn` | 无返回
 - 描述: 就地将拼接所提供的所有消息链拼接到当前实例的末尾.

#### MessageChain.plusWith

(method) MessageChain.**plusWith**(**chains*: `MessageChain`)
 - 返回值类型: `MessageChain`
 - 描述: 将拼接所提供的所有消息链拼接到当前实例的末尾, 并返回一个新的消息链实例.

#### MessageChain.asDisplay

(method) MessageChain.**asDisplay**()
 - 返回值类型: `str`
 - 描述: 将当前消息链用字符串表达, 但 `Image` 等元素会变成类似 `[图片]` 这样的形式, 以此本方法只能用于简单的匹配.

#### MessageChain.isImmutable

(priority) MessageChain.**isImmutable**
 - 返回值类型: `bool`
 - 描述: 检查当前消息链是否可变.

#### MessageChain.isSendable

(priority) MessageChain.**isSendable**
 - 返回值类型: `bool`
 - 描述: 检查当前消息链是否可发送.

#### MessageChain.asMutable

(method) MessageChain.**asMutable**()
 - 返回值类型: `MessageChain`
 - 描述: 将当前消息链作为可变形式的新实例返回.

#### MessageChain.asImmutable

(method) MessageChain.**asImmutable**()
 - 返回值类型: `MessageChain`
 - 描述: 将当前消息链作为不可变形式的新实例返回.

#### MessageChain.asSendable

(method) MessageChain.**asSendable**()
 - 返回值类型: `MessageChain`
 - 描述: 将当前消息链中的不可发送的元素去除, 并返回一个新实例.