Module graia.application.message.parser.kanata
==============================================

Functions
---------

    
`origin_or_zero(origin: Union[~_T, NoneType]) ‑> Union[~_T, int]`
:   

Classes
-------

`Kanata(signature_list: List[Union[graia.application.message.parser.signature.NormalMatch, graia.application.message.parser.signature.PatternReceiver]], stop_exec_if_fail: bool = True, allow_quote: bool = True, skip_one_at_in_quote: bool = False)`
:   彼方.
    
    该魔法方法用于实例化该参数解析器.
    
    Args:
        signature_list (List[Union[NormalMatch, PatternReceiver]]): 匹配标识链
        stop_exec_if_fail (bool, optional): 是否在无可用匹配时停止监听器执行. Defaults to True.
        allow_quote (bool, optional): 是否允许 Kanata 处理回复消息中的用户输入部分. Defaults to True.
        skip_one_at_in_quote (bool, optional): 是否允许 Kanata 在处理回复消息中的用户输入部分时自动删除可能                由 QQ 客户端添加的 At 和一个包含在单独 Plain 元素中的空格. Defaults to False.

    ### Ancestors (in MRO)

    * graia.broadcast.builtin.factory.AsyncDispatcherContextManager
    * graia.broadcast.entities.dispatcher.BaseDispatcher

    ### Class variables

    `allow_quote: bool`
    :

    `args`
    :

    `kwargs`
    :

    `parsed_items: Dict[str, graia.application.message.chain.MessageChain]`
    :

    `signature_list: List[Union[graia.application.message.parser.signature.NormalMatch, graia.application.message.parser.signature.PatternReceiver]]`
    :

    `skip_one_at_in_quote: bool`
    :

    `stop_exec_if_fail: bool`
    :

    ### Static methods

    `allocation(mapping: Dict[graia.application.message.parser.pack.Arguments, graia.application.message.chain.MessageChain]) ‑> Union[Dict[str, graia.application.message.chain.MessageChain], NoneType]`
    :

    `detect_and_mapping(signature_chain: Tuple[Union[graia.application.message.parser.signature.NormalMatch, graia.application.message.parser.signature.PatternReceiver]], message_chain: graia.application.message.chain.MessageChain) ‑> Union[Dict[graia.application.message.parser.pack.Arguments, graia.application.message.chain.MessageChain], NoneType]`
    :

    `detect_index(signature_chain: Tuple[Union[graia.application.message.parser.signature.NormalMatch, graia.application.message.parser.signature.PatternReceiver]], message_chain: graia.application.message.chain.MessageChain) ‑> Union[Dict[str, Tuple[Tuple[int, Union[int, NoneType]], Tuple[int, Union[int, NoneType]]]], NoneType]`
    :

    ### Methods

    `catch_argument_names(self) ‑> List[str]`
    :

    `generator_factory(self) ‑> Callable[[Any], AsyncGenerator[Union[NoneType, Tuple[Literal[<ResponseCodeEnum.VALUE: 1>], Any]], Union[NoneType, Tuple[graia.broadcast.builtin.factory.StatusCodeEnum, graia.broadcast.builtin.factory.ExcInfo]]]]`
    :