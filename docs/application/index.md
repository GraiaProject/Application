Module graia.application
========================

Sub-modules
-----------
* graia.application.context
* graia.application.entities
* graia.application.entry
* graia.application.event
* graia.application.exceptions
* graia.application.friend
* graia.application.group
* graia.application.interrupts
* graia.application.logger
* graia.application.message
* graia.application.session
* graia.application.test
* graia.application.utilles

Functions
---------

    
`error_wrapper(network_action_callable: Callable)`
:   

Classes
-------

`GraiaMiraiApplication(*, broadcast: Union[graia.broadcast.Broadcast, NoneType], connect_info: graia.application.session.Session, session: Union[aiohttp.client.ClientSession, NoneType] = None, logger: Union[graia.application.logger.AbstractLogger, NoneType] = None, debug: bool = False, enable_chat_log: bool = True, group_message_log_format: str = '{bot_id}: [{group_name}({group_id}] {member_name}({member_id}) -> {message_string}', friend_message_log_format: str = '{bot_id}: [{friend_name}({friend_id})] -> {message_string}', temp_message_log_format: str = '{bot_id}: [{group_name}({group_id}.{member_name}({member_id})] -> {message_string}', json_loader: Callable[[Any], Any] = <function loads>)`
:   本类的实例即 应用实例(Application), 是面向 `mirai-api-http` 接口的实际功能实现.
    你的应用大多都围绕着本类及本类的实例展开.
    
    Attributes:
        broadcast (Broadcast): 被指定的, 外置的事件系统, 即 `Broadcast Control`,
            通常你不需要干涉该属性;
        session (ClientSession): 即 `aiohttp.ClientSession` 的实例, 用于与 `mirai-api-http` 通讯.
        connect_info (Session): 用于描述会话对象, 其中最重要的属性是 `sessionKey`, 用于存储当前的会话标识.
        logger (AbstractLogger): 日志系统实现类的实例, 默认以 `logging` 为日志驱动.

    ### Static methods

    `auto_parse_by_type(original_dict: dict) ‑> graia.broadcast.entities.event.BaseEvent`
    :   从尚未明确指定事件类型的对象中获取事件的定义, 并进行解析
        
        Args:
            original_dict (dict): 用 dict 表示的序列化态事件, 应包含有字段 `type` 以供分析事件定义.
        
        Raises:
            InvaildArgument: 目标对象中不包含字段 `type`
            ValueError: 没有找到对应的字段, 通常的, 这意味着应用获取到了一个尚未被定义的事件, 请报告问题.
        
        Returns:
            BaseEvent: 已经被序列化的事件

    ### Instance variables

    `broadcast: Union[graia.broadcast.Broadcast, NoneType]`
    :   Return an attribute of instance, which is of type owner.

    `chat_log_enabled: bool`
    :   Return an attribute of instance, which is of type owner.

    `connect_info: graia.application.session.Session`
    :   Return an attribute of instance, which is of type owner.

    `debug: bool`
    :   Return an attribute of instance, which is of type owner.

    `friend_message_log_format: str`
    :   Return an attribute of instance, which is of type owner.

    `group_message_log_format: str`
    :   Return an attribute of instance, which is of type owner.

    `json_loader: Callable[[Any], Any]`
    :   Return an attribute of instance, which is of type owner.

    `logger: graia.application.logger.AbstractLogger`
    :   Return an attribute of instance, which is of type owner.

    `session: aiohttp.client.ClientSession`
    :   Return an attribute of instance, which is of type owner.

    `temp_message_log_format: str`
    :   Return an attribute of instance, which is of type owner.

    ### Methods

    `activeSession(self) ‑> NoReturn`
    :   激活当前已经存入 connect_info 的会话标识,
        如果没有事先调用 `authenticate` 方法获取未激活的会话标识, 则会触发 `InvaildSession` 错误.
        
        Raises:
            InvaildSession: 没有事先调用 `authenticate` 方法获取未激活的会话标识
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `authenticate(self) ‑> str`
    :   从路由 `/auth` 下获取尚未被激活的会话标识并返回; 通常的, 你还需要使用 `activeSession` 方法激活它.
        
        Returns:
            str: 即返回的会话标识

    `countMessage(self) ‑> int`
    :   获取 `mirai-api-http` 内部缓存中的消息的数量
        
        Returns:
            int: 缓存中的消息的数量

    `fetchLatestMessage(self, count: int = 10) ‑> List[Union[graia.application.event.messages.GroupMessage, graia.application.event.messages.TempMessage, graia.application.event.messages.FriendMessage]]`
    :

    `fetchMessage(self, count: int = 10) ‑> List[Union[graia.application.event.messages.GroupMessage, graia.application.event.messages.TempMessage, graia.application.event.messages.FriendMessage]]`
    :   从路由 `/fetchMessage` 处获取指定数量的消息; 当关闭 Websocket 时, 该方法被用于获取事件.
        
        Args:
            count (int, optional): 消息获取的数量. 默认为 10.
        
        Returns:
            List[Union[GroupMessage, TempMessage, FriendMessage]]: 获取到的消息

    `friendList(self) ‑> List[graia.application.friend.Friend]`
    :   获取当前会话账号所拥有的所有好友的信息
        
        Returns:
            List[Friend]: 当前会话账号所拥有的所有好友的信息

    `getConfig(self) ‑> graia.application.entities.MiraiConfig`
    :   获取 mirai-api-http 中维护的当前会话的配置.
        
        Returns:
            MiraiConfig: 当前会话的配置

    `getFetching(self)`
    :

    `getFriend(self, friend_id: int) ‑> Union[graia.application.friend.Friend, NoneType]`
    :   从已知的可能的好友 ID, 获取 Friend 实例.
        
        Args:
            friend_id (int): 已知的可能的好友 ID.
        
        Returns:
            Friend: 操作成功, 你得到了你应得的.
            None: 未能获取到.

    `getGroup(self, group_id: int) ‑> Union[graia.application.group.Group, NoneType]`
    :   尝试从已知的群组唯一ID, 获取对应群组的信息; 可能返回 None.
        
        Args:
            group_id (int): 尝试获取的群组的唯一 ID.
        
        Returns:
            Group: 操作成功, 你得到了你应得的.
            None: 未能获取到.

    `getGroupConfig(self, group: Union[graia.application.group.Group, int]) ‑> graia.application.group.GroupConfig`
    :   获取指定群组的群设置
        
        Args:
            group (Union[Group, int]): 需要获取群设置的指定群组
        
        Returns:
            GroupConfig: 指定群组的群设置

    `getMember(self, group: Union[graia.application.group.Group, int], member_id: int) ‑> Union[graia.application.group.Member, NoneType]`
    :   尝试从已知的群组唯一 ID 和已知的群组成员的 ID, 获取对应成员的信息; 可能返回 None.
        
        Args:
            group_id (Union[Group, int]): 已知的群组唯一 ID
            member_id (int): 已知的群组成员的 ID
        
        Returns:
            Member: 操作成功, 你得到了你应得的.
            None: 未能获取到.

    `getMemberInfo(self, member: Union[graia.application.group.Member, int], group: Union[graia.application.group.Group, int, NoneType] = None) ‑> graia.application.group.MemberInfo`
    :   获取指定群组成员的可修改状态.
        
        Args:
            member (Union[Member, int]): 指定群成员, 可为 Member 实例, 若前设成立, 则不需要提供 group.
            group (Optional[Union[Group, int]], optional): 如果 member 为 Member 实例, 则不需要提供本项, 否则需要. 默认为 None.
        
        Raises:
            TypeError: 提供了错误的参数, 阅读有关文档得到问题原因
        
        Returns:
            MemberInfo: 指定群组成员的可修改状态

    `getVersion(self, auto_set=True) ‑> Tuple`
    :   从 `/about` 路由下获取当前使用的 `mirai-api-http` 版本, 注意, 该 API 并不是一开始就有的(1.6.2 版本才支持本接口).
        
        Args:
            auto_set (bool, optional): 是否自动将版本存入 connect_info 以判断接口是否有效. Defaults to True.
        
        Returns:
            Tuple: 以元组形式表示的版本信息.

    `groupList(self) ‑> List[graia.application.group.Group]`
    :   获取当前会话账号所加入的所有群组的信息.
        
        Returns:
            List[Group]: 当前会话账号所加入的所有群组的信息

    `http_fetchmessage_poster(self, delay=0.5, fetch_num=10)`
    :

    `initialize(self)`
    :

    `initializeFetchingTask(self) ‑> _asyncio.Task`
    :

    `kick(self, group: Union[graia.application.group.Group, int], member: Union[graia.application.group.Member, int], message: Union[str, NoneType] = None) ‑> NoReturn`
    :   将目标群组成员从指定群组删除; 需要具有相应权限(管理员/群主)
        
        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
            message (Optional[str], optional): 如果给出, 则作为该操作的利益并向对象展示; 在当前版本中, 指定本参数无效. 默认为 None.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `launch_blocking(self, loop: Union[asyncio.events.AbstractEventLoop, NoneType] = None)`
    :

    `logger_friend_message(self, event: graia.application.event.messages.FriendMessage)`
    :

    `logger_group_message(self, event: graia.application.event.messages.GroupMessage)`
    :

    `logger_temp_message(self, event: graia.application.event.messages.TempMessage)`
    :

    `memberList(self, group: Union[graia.application.group.Group, int]) ‑> List[graia.application.group.Member]`
    :   获取群组中所有群组成员的信息
        
        Args:
            group (Union[Group, int]): 群组/群组ID
        
        Returns:
            List[Member]: 即群组中所有成员的可被获取到的信息.

    `messageFromId(self, source: Union[graia.application.message.elements.internal.Source, int]) ‑> Union[graia.application.event.messages.GroupMessage, graia.application.event.messages.TempMessage, graia.application.event.messages.FriendMessage]`
    :   尝试从已知的 `messageId` 获取缓存中的消息
        
        Args:
            source (Union[Source, int]): 需要获取的消息的 `messageId`
        
        Returns:
            Union[GroupMessage, TempMessage, FriendMessage]: 获取到的消息

    `modifyConfig(self, *, cacheSize: Union[int, NoneType] = None, enableWebsocket: Union[bool, NoneType] = None) ‑> NoReturn`
    :   修改当前会话的配置
        
        Args:
            cacheSize (Optional[int], optional): 缓存消息的条数. Defaults to None.
            enableWebsocket (Optional[bool], optional): 是否启用 Websocket 方式获取事件. Defaults to None.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `modifyGroupConfig(self, group: Union[graia.application.group.Group, int], config: graia.application.group.GroupConfig) ‑> NoReturn`
    :   修改指定群组的群设置; 需要具有相应权限(管理员/群主).
        
        Args:
            group (Union[Group, int]): 需要修改群设置的指定群组
            config (GroupConfig): 经过修改后的群设置
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `modifyMemberInfo(self, member: Union[graia.application.group.Member, int], info: graia.application.group.MemberInfo, group: Union[graia.application.group.Group, int, NoneType] = None) ‑> NoReturn`
    :   修改指定群组成员的可修改状态; 需要具有相应权限(管理员/群主).
        
        Args:
            member (Union[Member, int]): 指定的群组成员, 可为 Member 实例, 若前设成立, 则不需要提供 group.
            info (MemberInfo): 已修改的指定群组成员的可修改状态
            group (Optional[Union[Group, int]], optional): 如果 member 为 Member 实例, 则不需要提供本项, 否则需要. 默认为 None.
        
        Raises:
            TypeError: 提供了错误的参数, 阅读有关文档得到问题原因
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `mute(self, group: Union[graia.application.group.Group, int], member: Union[graia.application.group.Member, int], time: int) ‑> NoReturn`
    :   在指定群组禁言指定群成员; 需要具有相应权限(管理员/群主); `time` 不得大于 `30*24*60*60=2592000` 或小于 `0`, 否则会自动修正;
        当 `time` 小于等于 `0` 时, 不会触发禁言操作; 禁言对象极有可能触发 `PermissionError`, 在这之前请对其进行判断!
        
        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
            time (int): 禁言事件, 单位秒, 修正规则: `{time|0 < time <= 2592000}`
        
        Raises:
            PermissionError: 没有相应操作权限.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `muteAll(self, group: Union[graia.application.group.Group, int]) ‑> NoReturn`
    :   在指定群组开启全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)
        
        Args:
            group (Union[Group, int]): 指定的群组.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `peekLatestMessage(self, count: int = 10) ‑> List[Union[graia.application.event.messages.GroupMessage, graia.application.event.messages.TempMessage, graia.application.event.messages.FriendMessage]]`
    :

    `peekMessage(self, count: int = 10) ‑> List[Union[graia.application.event.messages.GroupMessage, graia.application.event.messages.TempMessage, graia.application.event.messages.FriendMessage]]`
    :

    `quit(self, group: Union[graia.application.group.Group, int]) ‑> NoReturn`
    :   主动从指定群组退出
        
        Args:
            group (Union[Group, int]): 需要退出的指定群组
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `revokeMessage(self, target: Union[graia.application.message.elements.internal.Source, graia.application.message.BotMessage, int]) ‑> NoReturn`
    :   撤回特定的消息; 撤回自己的消息需要在发出后 2 分钟内才能成功撤回; 如果在群组内, 需要撤回他人的消息则需要管理员/群主权限.
        
        Args:
            target (Union[Source, BotMessage, int]): 特定信息的 `messageId`, 可以是 `Source` 实例, `BotMessage` 实例或者是单纯的 int 整数.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `sendFriendMessage(self, target: Union[graia.application.friend.Friend, int], message: graia.application.message.chain.MessageChain, *, quote: Union[graia.application.message.elements.internal.Source, int, NoneType] = None) ‑> graia.application.message.BotMessage`
    :   发送消息给好友, 可以指定回复的消息.
        
        Args:
            target (Union[Friend, int]): 指定的好友
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.
        
        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.

    `sendGroupMessage(self, group: Union[graia.application.group.Group, int], message: graia.application.message.chain.MessageChain, *, quote: Union[graia.application.message.elements.internal.Source, int, NoneType] = None) ‑> graia.application.message.BotMessage`
    :   发送消息到群组内, 可以指定回复的消息.
        
        Args:
            group (Union[Group, int]): 指定的群组, 可以是群组的 ID 也可以是 Group 实例.
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.
        
        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.

    `sendTempMessage(self, group: Union[graia.application.group.Group, int], target: Union[graia.application.group.Member, int], message: graia.application.message.chain.MessageChain, *, quote: Union[graia.application.message.elements.internal.Source, int, NoneType] = None) ‑> graia.application.message.BotMessage`
    :   发送临时会话给群组中的特定成员, 可指定回复的消息.
        
        Args:
            group (Union[Group, int]): 指定的群组, 可以是群组的 ID 也可以是 Group 实例.
            target (Union[Member, int]): 指定的群组成员, 可以是成员的 ID 也可以是 Member 实例.
            message (MessageChain): 有效的, 可发送的(Sendable)消息链.
            quote (Optional[Union[Source, int]], optional): 需要回复的消息, 不要忽视我啊喂?!!, 默认为 None.
        
        Returns:
            BotMessage: 即当前会话账号所发出消息的元数据, 内包含有一 `messageId` 属性, 可用于回复.

    `shutdown(self)`
    :

    `signout(self) ‑> NoReturn`
    :   释放当前激活/未激活的会话标识
        
        Raises:
            InvaildSession: 没有事先调用 `authenticate` 方法获取会话标识
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `switch_event_detect_method(self)`
    :

    `unmute(self, group: Union[graia.application.group.Group, int], member: Union[graia.application.group.Member, int]) ‑> NoReturn`
    :   在指定群组解除对指定群成员的禁言; 需要具有相应权限(管理员/群主); 对象极有可能触发 `PermissionError`, 在这之前请对其进行判断!
        
        Args:
            group (Union[Group, int]): 指定的群组
            member (Union[Member, int]): 指定的群成员(只能是普通群员或者是管理员, 后者则要求群主权限)
        
        Raises:
            PermissionError: 没有相应操作权限.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `unmuteAll(self, group: Union[graia.application.group.Group, int]) ‑> NoReturn`
    :   在指定群组关闭全体禁言, 需要当前会话账号在指定群主有相应权限(管理员或者群主权限)
        
        Args:
            group (Union[Group, int]): 指定的群组.
        
        Returns:
            NoReturn: 没有有意义的返回, 或者说, 返回 `None` 就代表这个操作成功了.

    `uploadImage(self, image_bytes: bytes, method: graia.application.entities.UploadMethods, return_external: bool = False) ‑> Union[graia.application.message.elements.internal.Image, graia.application.message.elements.external.Image]`
    :   上传一张图片到远端服务器, 需要提供: 图片的原始数据(bytes), 图片的上传类型; 你可以控制是否返回外部态的 Image 消息元素.
        Args:
            image_bytes (bytes): 图片的原始数据
            method (UploadMethods): 图片的上传类型
            return_external (bool, optional): 是否返回外部态的 Image 消息元素. 默认为 False.
        Returns:
            Image(internal): 内部态的 Image 消息元素
            Image(external): 外部态的 Image 消息元素

    `uploadVoice(self, voice_bytes: bytes, method: graia.application.entities.UploadMethods = UploadMethods.Group, return_external: bool = False) ‑> Union[graia.application.message.elements.internal.Voice, graia.application.message.elements.external.Voice]`
    :   上传一份语音数据(类型为原始 bytes)到远端服务器, 需要提供: 语音的原始数据(bytes), 语音的上传类型(默认为 Group); 你可以控制是否返回外部态的 Voice 消息元素.
        
        Args:
            voice_bytes (bytes): 语音的原始数据
            method (UploadMethods): 语音的上传类型, 默认为 `UploadMethods.Group`.
            return_external (bool, optional): 是否返回外部态的 Voice 消息元素. 默认为 False.
        
        Returns:
            Voice(internal): 内部态的 Voice 消息元素
            Voice(external): 外部态的 Voice 消息元素

    `url_gen(self, path) ‑> str`
    :   从 connect_info 和 path 生成接口的地址.
        
        Args:
            path (str): 需求的接口地址
        
        Returns:
            str: 作为结果的地址

    `websocket_daemon(self)`
    :

    `ws_all_poster(self)`
    :

    `ws_ping(self, ws_connect: aiohttp.client_ws.ClientWebSocketResponse, delay: float = 30.0)`
    :