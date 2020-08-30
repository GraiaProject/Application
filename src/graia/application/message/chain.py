from __future__ import annotations
from typing import (Any, Dict, List, NoReturn, Sequence, Tuple, Type, Union, Optional)

from graia.application.exceptions import EntangledSuperposition
from graia.broadcast.utilles import run_always_await
from pydantic import BaseModel

from .elements import ExternalElement, InternalElement, Element
import regex
import copy

T = Element
MessageIndex = Tuple[int, Optional[int]]

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
        12. `MessageChain.asSerializationString` 方法可将消息链对象转为以 "Mirai 码" 表示特殊对象的字符串
        13. `MessageChain.fromSerializationString` 方法可以从以 "Mirai 码" 表示特殊对象的字符串解析为消息链, 不过可能不完整.
        14. `MessageChain.asMerged` 方法可以将消息链中相邻的 Plain 元素合并为一个 Plain 元素.
        15. 你可以通过一个分片实例取项, 这个分片的 `start` 和 `end` 的 Type Annotation 都是 `Optional[MessageIndex]`:
        ``` python
        message = MessageChain.create([
            Plain("123456789"), At(123), Plain("3423")
        ])
        message.asMerged()[(0, 12):] # => [At(123), Plain("3423")]
        ```
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

    def get(self, element_class: Type[Element]) -> List[T]:
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

    def __getitem__(self, item: Union[Type[Element], slice]):
        if isinstance(item, slice):
            return self.subchain(item)
        elif issubclass(item, Element):
            return self.get(item)
        else:
            raise NotImplementedError("{0} is not allowed for item getting".format(type(item)))

    def subchain(self, item: slice) -> "MessageChain":
        """对消息链执行分片操作

        Args:
            item (slice): 这个分片的 `start` 和 `end` 的 Type Annotation 都是 `Optional[MessageIndex]`

        Raises:
            TypeError: TextIndex 取到了错误的位置

        Returns:
            MessageChain: 分片后得到的新消息链, 绝对是原消息链的子集.
        """
        from .elements.internal import Plain
        result = copy.copy(self.__root__)
        if item.start:
            first_slice = result[item.start[0]:]
            if item.start[1] is not None and first_slice: # text slice
                if not isinstance(first_slice[0], Plain):
                    raise TypeError("the sliced chain does not starts with a Plain: {}".format(first_slice[0]))
                final_text = first_slice[0].text[item.start[1]:]
                result = [
                    *([Plain(final_text)] if final_text else []),
                    *first_slice[1:]
                ]
            else:
                result = first_slice
        if item.stop:
            first_slice = result[:item.stop[0]]
            if item.stop[1] is not None and first_slice: # text slice
                if not isinstance(first_slice[-1], Plain):
                    raise TypeError("the sliced chain does not ends with a Plain: {}".format(first_slice[-1]))
                final_text = first_slice[-1].text[:item.stop[1]]
                result = [
                    *first_slice[:-1],
                    *([Plain(final_text)] if final_text else [])
                ]
            else:
                result = first_slice
        return MessageChain.create(result)

    def asSerializationString(self) -> str:
        """将消息链对象转为以 "Mirai 码" 表示特殊对象的字符串

        Returns:
            str: 以 "Mirai 码" 表示特殊对象的字符串
        """
        return "".join([i.asSerializationString() for i in self.__root__])
    
    @classmethod
    def fromSerializationString(cls, string: str) -> "MessageChain":
        """将以 "Mirai 码" 表示特殊对象的字符串转为消息链对象

        Returns:
            MessageChain: 转换后得到的消息链, 所包含的信息可能不完整.
        """
        from .elements.internal import Source, Plain, AtAll, At, Face, Image, FlashImage
        code_without_argument = {
            "atall": AtAll
        }
        origin_list = list(regex.finditer(
            r"((?:\[mirai:(?P<name>[^:]+)\])|(?:\[mirai:(?P<name>[^\]]*)?:(?P<argument>.*?)?\]))|(?P<plaintext>.{1,})", string))

        result = [] # 默认为不可变型, 但这里要插入元素
        for i in origin_list:
            origin_pattern = i.groupdict()
            if origin_pattern['name'] and not origin_pattern['argument']: # 无参数型
                target_element = code_without_argument.get(origin_pattern['name'])
                if target_element:
                    result.append(target_element())
            elif origin_pattern['name'] and origin_pattern['argument']: # 有参数
                arguments = origin_pattern['argument'].split(",")
                if origin_pattern['name'] == "source":
                    result.append(Source(id=int(arguments[0]), time=arguments[1]))
                elif origin_pattern['name'] == "at":
                    result.append(At(target=int(arguments[0]), display=arguments[1]))
                elif origin_pattern['name'] == "face":
                    result.append(Face(faceId=int(arguments[0])))
                elif origin_pattern['name'] == "image":
                    result.append(Image(imageId=origin_pattern['argument']))
                elif origin_pattern['name'] == "flash":
                    result.append(FlashImage(imageId=origin_pattern['argument']))
            elif origin_pattern['plaintext']:
                result.append(Plain(origin_pattern['plaintext']))
        return cls.create(tuple(result))

    def asMerged(self) -> "MessageChain":
        """合并相邻的 Plain 项, 并返回一个新的消息链实例
        
        Returns:
            MessageChain: 得到的新的消息链实例, 里面不应存在有任何的相邻的 Plain 元素.
        """
        from .elements.internal import Plain
        result = []

        plain = []
        for i in self.__root__:
            if not isinstance(i, Plain):
                if plain:
                    result.append(Plain("".join(plain)))
                    plain.clear() # 清空缓存
                result.append(i)
            else:
                plain.append(i.text)
        else:
            if plain:
                result.append(Plain("".join(plain)))
                plain.clear() # 清空缓存
        return MessageChain.create(type(self.__root__)(result)) # 维持 Mutable
    
    def exclude(self, *types: Type[Element]) -> MessageChain:
        """将除了在给出的消息元素类型中符合的消息元素重新包装为一个新的消息链

        Args:
            *types (Type[Element]): 将排除在外的消息元素类型

        Returns:
            MessageChain: 返回的消息链中不包含参数中给出的消息元素类型
        """
        return self.create(type(self.__root__)([
            i for i in self.__root__ if type(i) not in types
        ]))
    
    def include(self, *types: Type[Element]) -> MessageChain:
        """将只在给出的消息元素类型中符合的消息元素重新包装为一个新的消息链

        Args:
            *types (Type[Element]): 将只包含在内的消息元素类型

        Returns:
            MessageChain: 返回的消息链中只包含参数中给出的消息元素类型
        """
        return self.create(type(self.__root__)([
            i for i in self.__root__ if type(i) in types
        ]))