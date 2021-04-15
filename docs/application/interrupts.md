Module graia.application.interrupts
===================================

Functions
---------

    
`FriendMessageInterrupt(special_friend: Union[graia.application.friend.Friend, int, NoneType] = None, quote_access: Union[graia.application.message.BotMessage, graia.application.message.elements.internal.Source, NoneType] = None, custom_judgement: Union[Callable[[graia.application.event.messages.FriendMessage], bool], NoneType] = None, block_propagation: bool = False)`
:   

    
`GroupMessageInterrupt(special_group: Union[graia.application.group.Group, int, NoneType] = None, special_member: Union[graia.application.group.Member, int, NoneType] = None, quote_access: Union[graia.application.message.BotMessage, graia.application.message.elements.internal.Source, NoneType] = None, custom_judgement: Union[Callable[[graia.application.event.messages.GroupMessage], bool], NoneType] = None, block_propagation: bool = False)`
:   

    
`TempMessageInterrupt(special_group: Union[graia.application.group.Group, int, NoneType] = None, special_member: Union[graia.application.group.Member, int, NoneType] = None, quote_access: Union[graia.application.message.BotMessage, graia.application.message.elements.internal.Source, NoneType] = None, custom_judgement: Union[Callable[[graia.application.event.messages.TempMessage], bool], NoneType] = None, block_propagation: bool = False)`
: