Module graia.broadcast.entities.dispatcher
==========================================

Classes
-------

`BaseDispatcher()`
:   所有非单函数型 Dispatcher 的基类, 用于为参数解析提供可扩展的支持.

    ### Descendants

    * graia.application.event.ApplicationDispatcher
    * graia.application.event.EmptyDispatcher
    * graia.application.event.dispatcher.MessageChainCatcher
    * graia.application.event.lifecycle.ApplicationLaunched.Dispatcher
    * graia.application.event.lifecycle.ApplicationLaunchedBlocking.Dispatcher
    * graia.application.event.lifecycle.ApplicationShutdowned.Dispatcher
    * graia.application.event.messages.Forward.Dispatcher
    * graia.application.event.messages.FriendMessage.Dispatcher
    * graia.application.event.messages.GroupMessage.Dispatcher
    * graia.application.event.messages.SourceElementDispatcher
    * graia.application.event.messages.TempMessage.Dispatcher
    * graia.application.event.mirai.BotJoinGroupEvent.Dispatcher
    * graia.application.event.mirai.BotLeaveEventActive.Dispatcher
    * graia.application.event.mirai.BotLeaveEventKick.Dispatcher
    * graia.application.event.mirai.BotMuteEvent.Dispatcher
    * graia.application.event.mirai.BotUnmuteEvent.Dispatcher
    * graia.application.event.mirai.GroupAllowAnonymousChatEvent.Dispatcher
    * graia.application.event.mirai.GroupAllowConfessTalkEvent.Dispatcher
    * graia.application.event.mirai.GroupAllowMemberInviteEvent.Dispatcher
    * graia.application.event.mirai.GroupEntranceAnnouncementChangeEvent.Dispatcher
    * graia.application.event.mirai.GroupMuteAllEvent.Dispatcher
    * graia.application.event.mirai.GroupNameChangeEvent.Dispatcher
    * graia.application.event.mirai.GroupRecallEvent.Dispatcher
    * graia.application.event.mirai.MemberCardChangeEvent.Dispatcher
    * graia.application.event.mirai.MemberJoinEvent.Dispatcher
    * graia.application.event.mirai.MemberLeaveEventKick.Dispatcher
    * graia.application.event.mirai.MemberLeaveEventQuit.Dispatcher
    * graia.application.event.mirai.MemberMuteEvent.Dispatcher
    * graia.application.event.mirai.MemberPermissionChangeEvent.Dispatcher
    * graia.application.event.mirai.MemberSpecialTitleChangeEvent.Dispatcher
    * graia.application.event.mirai.MemberUnmuteEvent.Dispatcher
    * graia.application.message.parser.literature.Literature
    * graia.application.utilles.AppMiddlewareAsDispatcher
    * graia.broadcast.builtin.event.ExceptionThrowed.Dispatcher
    * graia.broadcast.builtin.factory.AsyncDispatcherContextManager
    * graia.broadcast.builtin.factory.DispatcherContextManager
    * graia.broadcast.interfaces.decorator.DecoratorInterface
    * graia.broadcast.interfaces.dispatcher.EmptyEvent.Dispatcher
    * graia.saya.event.SayaModuleInstalled.Dispatcher
    * graia.saya.event.SayaModuleUninstall.Dispatcher
    * graia.saya.event.SayaModuleUninstalled.Dispatcher

    ### Class variables

    `mixin: List[graia.broadcast.entities.dispatcher.BaseDispatcher]`
    :   声明该 Dispatcher 所包含的来自其他 Dispatcher 提供的参数解析支持,
        若某参数该 Dispatcher 无法解析, 将跳转到该列表中并交由其中的 Dispatcher 进行解析,
        该列表中的 Dispatcher 全部被调用过且都不返回一有效值时才会将解析权交由其他的 Dispatcher.

    ### Static methods

    `catch(interface: DispatcherInterface)`
    :   该方法可以是 `staticmethod`, `classmethod` 亦或是普通的方法/函数.
        唯一的要求是 `Dispatcher.catch` 获取到的必须为一可调用异步 Callable.
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;

    ### Methods

    `afterDispatch(self, interface: DispatcherInterface, exception: Union[Exception, NoneType], tb: Union[traceback, NoneType])`
    :   生命周期钩子: 在参数被解析完后被调用
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;
            exception (Optional[Exception]): 可能存在的异常对象, 若为 None 则表示无异常被抛出, 执行顺利完成.
            tb (Optional[TracebackType]): 可能存在的异常堆栈对象, 若为 None 则表示无异常被抛出, 执行顺利完成.

    `afterExecution(self, interface: DispatcherInterface, exception: Union[Exception, NoneType], tb: Union[traceback, NoneType])`
    :   生命周期钩子: 在整个执行流程(包括参数解析)完成(包含因异常被抛出而退出)后被调用.
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;
            exception (Optional[Exception]): 可能存在的异常对象, 若为 None 则表示无异常被抛出, 执行顺利完成.
            tb (Optional[TracebackType]): 可能存在的异常堆栈对象, 若为 None 则表示无异常被抛出, 执行顺利完成.

    `afterTargetExec(self, interface: DispatcherInterface, exception: Union[Exception, NoneType], tb: Union[traceback, NoneType])`
    :   生命周期钩子: 在事件执行主体被执行完成后被调用.
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;
            exception (Optional[Exception]): 可能存在的异常对象, 若为 None 则表示无异常被抛出, 执行顺利完成.
            tb (Optional[TracebackType]): 可能存在的异常堆栈对象, 若为 None 则表示无异常被抛出, 执行顺利完成.

    `beforeDispatch(self, interface: DispatcherInterface)`
    :   生命周期钩子: 在解析参数前被调用
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;

    `beforeExecution(self, interface: DispatcherInterface)`
    :   生命周期钩子: 在整个执行流程(包括参数解析)开始前被调用
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;

    `beforeTargetExec(self, interface: DispatcherInterface)`
    :   生命周期钩子: 在参数解析完成后, 准备执行事件执行主体前被调用.
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;

    `onActive(self, interface: DispatcherInterface)`
    :   生命周期钩子: 在该 Dispatcher 可用于参数解析时被立即调用.
        
        Args:
            interface (DispatcherInterface): `Dispatcher` 服务的主要对象, 可以从其中获取以下信息:
             - 当前解析中的参数的信息;
             - 当前执行的信息, 比如正在处理的事件, `Listener`/`ExecTarget` etc.;