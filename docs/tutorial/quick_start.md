# Quick Start

## 前言

这里我们假设你已经参照 [ `mirai` ](https://github.com/mamoe/mirai) 和 [ `mirai-api-http` ](https://github.com/mamoe/mirai-api-http)
的 README, 通过类似 `mirai-console-wrapper` 或者 `miraiOK` 的方式启动了你的 `mirai-console` , 同时也安装了最新版本的 `mirai-api-http` 插件.  

!> **重要** 如果你使用时开发库出现了错误, 应先检查是否是 `Graia Framework` 的错误, 
确认之后, 请在我们的 [Github Issues](https://github.com/GraiaProject/Application/issues) 处汇报你的错误, 
我们会尽快处理问题

?> **说明** 如果你曾经使用过 [ `python-mirai` ](https://github.com/NatriumLab/python-mirai), 
你应该尽快迁移到 `Graia Framework` , 之前我们允若的 `python-mirai v4` 正是 `Graia Framework` , 
即后者是前者的继承.  
若你仍然执意使用 `python-mirai` , 你将 **不会** 受到我们的技术支持, 请铭记.

## 安装

``` bash
pip install graia-application-mirai
# 使用 poetry(推荐的方式)
poetry add graia-application-mirai
```

?> **提示** 为了使框架特性与协议实现分开, 我们将 `Graia Framework` 中使用的事件系统独立为了一个库
(我们会为其写文档的, 但现在我们专注于更新 `graia-application-mirai`), 
以方便开发者获取到新版本中我们提供的, 针对框架本身的特性支持.  
你可以通过以下指令获取到最新的事件系统更新

``` bash
pip install graia-broadcast --upgrade
# 使用 poetry
poetry update graia-broadcast
```

## 你与机器人历史性的第一次对话

现在我们需要协定好 `mirai-api-http` 的配置, 以便于接下来的说明.

根据 `mirai-api-http` 的相关文档, 我们可以得出这么一个配置文件的方案:

``` yaml
# file: mirai-client/plugins/MiraiAPIHTTP/setting.yml
authKey: graia-mirai-api-http-authkey # 你可以自己设定, 这里作为示范

# 可选，缓存大小，默认4096.缓存过小会导致引用回复与撤回消息失败
cacheSize: 4096

enableWebsocket: true # 启用 websocket 方式, 若使用 websocket 方式交互会得到更好的性能
host: '0.0.0.0' # httpapi 服务监听的地址, 错误的设置会造成 Graia Application 无法与其交互
port: 8080 # httpapi 服务监听的端口, 错误的设置会造成 Graia Application 无法与其交互
```

将以下代码保存到文件 `bot.py` 内, 确保该文件位于你的工作区内:

``` python
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio

from graia.application.protocol.entities.message.elements.internal import Plain
from graia.application.protocol.entities.targets.friend import Friend

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="graia-mirai-api-http-authkey", # 填入 authKey
        account=5234120587, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain(__root__=[
        Plain("Hello, World!")
    ]))

app.launch_blocking()
```

运行这段代码, 终端输出:

``` bash
[root@localhost] $ python src/test.py
[2020-07-25 21:42:11,929][INFO]: launching app...
[2020-07-25 21:42:11,960][INFO]: using websocket to receive event
[2020-07-25 21:42:11,964][INFO]: event reveiver running...
```

此时, 你可以向你的机器人发送一条好友消息:

<div class="panel-view">
  <div class="controls">
    <div class="circle red"></div>
    <div class="circle yellow"></div>
    <div class="circle green"></div>
    <div class="title">好友聊天</div>
  </div>
  <div class="content">
    <div class="chat-message shown">
      <div class="avatar" style="background-color: rgb(204, 0, 102); ">A</div>
      <div class="nickname">Alice</div>
      <div class="message-box">向这个世界问个好吧.</div>
    </div>
    <div class="chat-message shown">
      <div class="avatar" style="background-color: rgb(11, 135, 218); ">B</div>
      <div class="nickname">Bot</div>
      <div class="message-box">Hello, world!</div>
    </div>
  </div>
</div>

Excellent(非常好), 你的机器人迈出了至关重要的一步!