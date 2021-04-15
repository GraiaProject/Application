Module graia.application.message.chain
======================================

Classes
-------

`MessageChain(**data: Any)`
:   即 "消息链", 被用于承载整个消息内容的数据结构, 包含有一有序列表, 包含有继承了 Element 的各式类实例.
    
    Example:
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
    
        4. 你可以使用 `MessageChain.isSendable` 方法检查消息链是否可以被 **完整无误** 的发送.
    
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
            ) # -> MessageChain
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
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Static methods

    `create(elements: Sequence[Element]) ‑> MessageChain`
    :   从传入的序列(可以是元组 tuple, 也可以是列表 list) 创建消息链.
        
        Args:
            elements (Sequence[T]): 包含且仅包含消息元素的序列
        
        Returns:
            MessageChain: 以传入的序列作为所承载消息的消息链

    `fromSerializationString(string: str) ‑> MessageChain`
    :   将以 "Mirai 码" 表示特殊对象的字符串转为消息链对象
        
        Returns:
            MessageChain: 转换后得到的消息链, 所包含的信息可能不完整.

    `join(*chains: "'MessageChain'") ‑> MessageChain`
    :   拼接参数中给出的所有消息链
        
        Returns:
            MessageChain: 拼接结果

    `parse_obj(obj: List[Element]) ‑> MessageChain`
    :   内部接口, 会自动将作为外部态的消息元素转为内部态.
        
        Args:
            obj (List[T]): 需要反序列化的对象
        
        Returns:
            MessageChain: 内部承载有尽量有效的内部态消息元素的消息链

    ### Instance variables

    `isImmutable: bool`
    :   判断消息链是否不可变
        
        Returns:
            bool: 判断结果, `True` 为不可变, `False` 为可变

    `isSendable: bool`
    :   判断消息链是否可以被 sendGroupMessage 等发送消息的方法正确发送的方法, 注意, 这个方法并不是万能的.
        
        Returns:
            bool: 判断的结果, True 为可发送, False 则反之.

    ### Methods

    `asDisplay(self) ‑> str`
    :   获取以字符串形式表示的消息链, 且趋于通常你见到的样子.
        
        Returns:
            str: 以字符串形式表示的消息链

    `asHypertext(self) ‑> MessageChain`
    :

    `asImmutable(self) ‑> MessageChain`
    :   将消息链转换为不可变形态的消息链
        
        Returns:
            MessageChain: 内部消息结构不可变的消息链

    `asMerged(self) ‑> MessageChain`
    :   合并相邻的 Plain 项, 并返回一个新的消息链实例
        
        Returns:
            MessageChain: 得到的新的消息链实例, 里面不应存在有任何的相邻的 Plain 元素.

    `asMutable(self) ‑> MessageChain`
    :   将消息链转换为可变形态的消息链
        
        Returns:
            MessageChain: 内部消息结构可变的消息链

    `asSendable(self) ‑> MessageChain`
    :   将消息链尽量转换为能够为发送消息的方法正确发送的新消息链, 该方法不保证转换无误差性, 且不保证转化后是否可以被发送.
        
        Returns:
            MessageChain: 返回的可能可以正确发送的消息链.

    `asSerializationString(self) ‑> str`
    :   将消息链对象转为以 "Mirai 码" 表示特殊对象的字符串. 为了保证可逆，纯文本中的'['用'[_'替代
        
        Returns:
            str: 以 "Mirai 码" 表示特殊对象的字符串

    `build(self, **extra: Dict[InternalElement, Tuple[list, dict]]) ‑> MessageChain`
    :

    `endswith(self, string: str) ‑> bool`
    :

    `exclude(self, *types: Type[Element]) ‑> graia.application.message.chain.MessageChain`
    :   将除了在给出的消息元素类型中符合的消息元素重新包装为一个新的消息链
        
        Args:
            *types (Type[Element]): 将排除在外的消息元素类型
        
        Returns:
            MessageChain: 返回的消息链中不包含参数中给出的消息元素类型

    `get(self, element_class: Element) ‑> List[graia.application.message.elements.Element]`
    :   获取消息链中所有特定类型的消息元素
        
        Args:
            element_class (T): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.
        
        Returns:
            List[T]: 获取到的符合要求的所有消息元素; 另: 可能是空列表([]).

    `getFirst(self, element_class: Element) ‑> graia.application.message.elements.Element`
    :   获取消息链中第 1 个特定类型的消息元素
        
        Args:
            element_class (Type[Element]): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.
        
        Returns:
            T: 消息链第 1 个特定类型的消息元素

    `getOne(self, element_class: Element, index: int) ‑> graia.application.message.elements.Element`
    :   获取消息链中第 index + 1 个特定类型的消息元素
        
        Args:
            element_class (Type[Element]): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.
            index (int): 索引, 从 0 开始数
        
        Returns:
            T: 消息链第 index + 1 个特定类型的消息元素

    `has(self, element_class: Element) ‑> bool`
    :   判断消息链中是否含有特定类型的消息元素
        
        Args:
            element_class (T): 需要判断的消息元素的类型, 例如 "Plain", "At", "Image" 等.
        
        Returns:
            bool: 判断结果

    `hasText(self, string: str) ‑> bool`
    :   判定消息链内是否包括相应字符串
        
        Args:
            string (str): 需要判断的字符串
        
        Returns:
            bool: 是否包括

    `include(self, *types: Type[Element]) ‑> graia.application.message.chain.MessageChain`
    :   将只在给出的消息元素类型中符合的消息元素重新包装为一个新的消息链
        
        Args:
            *types (Type[Element]): 将只包含在内的消息元素类型
        
        Returns:
            MessageChain: 返回的消息链中只包含参数中给出的消息元素类型

    `plus(self, *chains: "'MessageChain'") ‑> NoReturn`
    :   在现有的基础上将另一消息链拼接到原来实例的尾部
        
        Raises:
            ValueError: 原有的消息链不可变, 需要转为可变形态.
        
        Returns:
            NoReturn: 本方法无返回.

    `plusWith(self, *chains: "'MessageChain'") ‑> MessageChain`
    :   在现有的基础上将另一消息链拼接到原来实例的尾部, 并生成, 返回新的实例.
        
        Returns:
            MessageChain: 拼接结果

    `split(self, pattern: str, raw_string: bool = False) ‑> List[MessageChain]`
    :   和 `str.split` 差不多, 提供一个字符串, 然后返回分割结果.
        
        Returns:
            List["MessageChain"]: 分割结果, 行为和 `str.split` 差不多.

    `startswith(self, string: str) ‑> bool`
    :

    `subchain(self, item: slice, ignore_text_index: bool = False) ‑> MessageChain`
    :   对消息链执行分片操作
        
        Args:
            item (slice): 这个分片的 `start` 和 `end` 的 Type Annotation 都是 `Optional[MessageIndex]`
        
        Raises:
            TypeError: TextIndex 取到了错误的位置
        
        Returns:
            MessageChain: 分片后得到的新消息链, 绝对是原消息链的子集.