from __future__ import annotations
from typing import (Dict, List, NoReturn, Sequence, Tuple, Type, Union)

from graia.application.exceptions import EntangledSuperposition
from graia.broadcast.utilles import run_always_await
from pydantic import BaseModel

from .elements import ExternalElement, InternalElement

T = Union[InternalElement, ExternalElement]

def raiser(error):
    raise error

class MessageChain(BaseModel):
    """即 "消息链", 被用于承载整个消息内容的数据结构, 包含有一有序列表, 包含有继承了 Element 的各式类实例.

    Examples:
    1. 你可以使用 `MessageChain.create` 方法创建一个消息链:
    ``` python
    MessageChain.create([
        Plain("这是盛放在这个消息链中的一个 Plain 元素")
    ])
    ```
    2. 你可以使用 `MessageChain.isImmutable` 方法判定消息链的可变型:
    ``` python
    print(message.isImmutable()) # 监听器获取到的消息链默认为 False.
    ```
    3. 你可以使用 `MessageChain.asMutable` 和 `MessageChain.asImmutable` 方法分别获得可变与不可变的消息链.
    4. 你可以使用 `MessageChain.isSendable` 方法检查消息链是否可以被 完整无误 的发送.
    5. 使用 `MessageChain.asSendable` 方法, 将自动过滤原消息链中的无法发送的元素, 并返回一个新的, 可被发送的消息链.
    6. `MessageChain.has` 方法可用于判断特定的元素类型是否存在于消息链中:
    ``` python
    print(message.has(At))
    # 使用 in 运算符也可以
    print(At in message)
    ```
    7. 可以使用 `MessageChain.get` 方法获取消息链中的所有特定类型的元素:
    ``` python
    print(message.get(Image)) # -> List[Image]
    # 使用类似取出列表中元素的形式也可以:
    print(message[Image]) # -> List[Image]
    ```
    8. 使用 `MessageChain.asDisplay` 方法可以获取到字符串形式表示的消息, 至于字面意思, 看示例:
    ``` python
    print(MessageChain.create([
        Plain("text"), At(123, display="某人"), Image(...)
    ]).asDisplay()) # -> "text@某人 [图片]"
    ```
    9. 使用 `MessageChain.join` 方法可以拼接多个消息链:
    ``` python
    MessageChain.join(
        message1, message2, message3, ...
    ) # -> total_message
    ```
    10. `MessageChain.plusWith` 方法将在现有的基础上将另一消息链拼接到原来实例的尾部, 并生成, 返回新的实例; 该方法不改变原有和传入的实例.
    11. `MessageChain.plus` 方法将在现有的基础上将另一消息链拼接到原来实例的尾部; 该方法更改了原有的实例, 并要求 `isMutable` 方法返回 `True` 才可以执行.
    """
    __root__: Union[List[T], Tuple[T]]

    @classmethod
    def create(cls, elements: Sequence[T]) -> "MessageChain":
        """从传入的序列(可以是元组 tuple, 也可以是列表 list) 创建消息链.

        Args:
            elements (Sequence[T]): 包含且仅包含消息元素的序列

        Returns:
            MessageChain: 以传入的序列作为所承载消息的消息链
        """
        return cls(__root__=elements)

    @classmethod
    def parse_obj(cls: Type['MessageChain'], obj: List[T]) -> 'MessageChain':
        """内部接口, 会自动将作为外部态的消息元素转为内部态.

        Args:
            obj (List[T]): 需要反序列化的对象

        Returns:
            MessageChain: 内部承载有尽量有效的内部态消息元素的消息链
        """
        handled_elements = []
        for i in obj:
            if isinstance(i, InternalElement):
                handled_elements.append(i)
            elif isinstance(i, ExternalElement):
                for ii in InternalElement.__subclasses__():
                    if ii.__name__ == i.__class__.__name__:
                        handled_elements.append(ii.fromExternal(i))
            elif isinstance(i, dict) and "type" in i:
                for ii in ExternalElement.__subclasses__():
                    if ii.__name__ == i['type']:
                        for iii in InternalElement.__subclasses__():
                            if iii.__name__ == i['type']:
                                handled_elements.append(iii.fromExternal(ii.parse_obj(i)))
        return cls(__root__=tuple(handled_elements)) # 默认是不可变型

    @property
    def isImmutable(self) -> bool:
        """判断消息链是否不可变

        Returns:
            bool: 判断结果, `True` 为不可变, `False` 为可变 
        """
        return isinstance(self.__root__, tuple)

    def asMutable(self) -> "MessageChain":
        """将消息链转换为可变形态的消息链

        Returns:
            MessageChain: 内部消息结构可变的消息链
        """
        return MessageChain(__root__=list(self.__root__))

    def asImmutable(self) -> "MessageChain":
        """将消息链转换为不可变形态的消息链

        Returns:
            MessageChain: 内部消息结构不可变的消息链
        """
        return MessageChain(__root__=tuple(self.__root__))

    @property
    def isSendable(self) -> bool:
        """判断消息链是否可以被 sendGroupMessage 等发送消息的方法正确发送的方法, 注意, 这个方法并不是万能的.

        Returns:
            bool: 判断的结果, True 为可发送, False 则反之.
        """
        return all(all([
            isinstance(i, (InternalElement, ExternalElement)),
            hasattr(i, "toExternal"),
            getattr(i.__class__, "toExternal") != InternalElement.toExternal
        ]) for i in self.__root__)

    def asSendable(self) -> "MessageChain":
        """将消息链尽量转换为能够为发送消息的方法正确发送的新消息链, 该方法不保证转换无误差性, 且不保证转化后是否可以被发送.

        Returns:
            MessageChain: 返回的可能可以正确发送的消息链.
        """
        return MessageChain(__root__=tuple([i for i in self.__root__ if all([
            isinstance(i, InternalElement),
            hasattr(i, "toExternal"),
            getattr(i.__class__, "toExternal") != InternalElement.toExternal
        ])]))

    async def build(self, **extra: Dict[InternalElement, Tuple[list, dict]]) -> "MessageChain":
        result = []
        for i in self.__root__:
            if isinstance(i, InternalElement):
                if getattr(i.__class__, "toExternal") == InternalElement.toExternal:
                    raise EntangledSuperposition("You define an object that cannot be sent: {0}".format(i.__class__.__name__))
                result.append(await run_always_await(i.toExternal(
                    *(extra[i.__class__][0] if i.__class__ in extra else []),
                    **(extra[i.__class__][1] if i.__class__ in extra else {})
                )))
            else:
                result.append(i)
        return MessageChain(__root__=tuple(result))

    def has(self, element_class: T) -> bool:
        """判断消息链中是否含有特定类型的消息元素

        Args:
            element_class (T): 需要判断的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            bool: 判断结果
        """
        return element_class in [type(i) for i in self.__root__]

    def get(self, element_class: T) -> List[T]:
        """获取消息链中所有特定类型的消息元素

        Args:
            element_class (T): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            List[T]: 获取到的符合要求的所有消息元素; 另: 可能是空列表([]).
        """
        return [i for i in self.__root__ if isinstance(i, element_class)]

    def asDisplay(self) -> str:
        """获取以字符串形式表示的消息链, 且趋于通常你见到的样子.

        Returns:
            str: 以字符串形式表示的消息链
        """
        return "".join(i.asDisplay() for i in self.__root__)

    @classmethod
    def join(cls, *chains: "MessageChain") -> "MessageChain":
        """拼接参数中给出的所有消息链

        Returns:
            MessageChain: 拼接结果
        """
        return cls.create(sum(chains, []))

    def plusWith(self, *chains: "MessageChain") -> "MessageChain":
        """在现有的基础上将另一消息链拼接到原来实例的尾部, 并生成, 返回新的实例.

        Returns:
            MessageChain: 拼接结果
        """
        return self.create(sum(chains, self.__root__))

    def plus(self, *chains: "MessageChain") -> NoReturn:
        """在现有的基础上将另一消息链拼接到原来实例的尾部

        Raises:
            ValueError: 原有的消息链不可变, 需要转为可变形态.

        Returns:
            NoReturn: 本方法无返回.
        """
        if self.isImmutable:
            raise ValueError("this chain is not mutable")
        for i in chains:
            self.__root__.extend(i.__root__)

    __contains__ = has
    __getitem__ = get