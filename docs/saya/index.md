Module graia.saya
=================

Sub-modules
-----------
* graia.saya.behaviour
* graia.saya.builtins
* graia.saya.channel
* graia.saya.context
* graia.saya.cube
* graia.saya.event
* graia.saya.schema

Classes
-------

`Saya(broadcast: graia.broadcast.Broadcast = None)`
:   Modular application for Graia Framework.
    
    > 名称取自作品 魔女之旅 中的角色 "沙耶(Saya)", 愿所有人的心中都有一位活泼可爱的炭之魔女.
    
    Saya 的架构分为: `Saya Controller`(控制器), `Module Channel`(模块容器), `Cube`(内容容器), `Behaviour`(行为).
    
     - `Saya Controller` 负责管理各个模块的
    
    Raises:
        TypeError: [description]
    
    Returns:
        [type]: [description]

    ### Class variables

    `behaviour_interface: graia.saya.behaviour.interface.BehaviourInterface`
    :

    `behaviours: List[graia.saya.behaviour.entity.Behaviour]`
    :

    `broadcast: Union[graia.broadcast.Broadcast, NoneType]`
    :

    `channels: Dict[str, graia.saya.channel.Channel]`
    :

    ### Static methods

    `current() ‑> graia.saya.Saya`
    :

    ### Methods

    `create_main_channel(self) ‑> graia.saya.channel.Channel`
    :

    `find_route(self, route: str) ‑> Any`
    :

    `install_behaviours(self, *behaviours: graia.saya.behaviour.entity.Behaviour)`
    :

    `module_context(self)`
    :

    `reload_channel(self, channel: graia.saya.channel.Channel = None, module: str = None) ‑> NoneType`
    :

    `require(self, module: str) ‑> Union[graia.saya.channel.Channel, Any]`
    :

    `require_resolve(self, module: str) ‑> graia.saya.channel.Channel`
    :

    `uninstall_channel(self, channel: graia.saya.channel.Channel)`
    :