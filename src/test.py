from devtools import debug
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.application.protocol import UploadMethods
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio
from graia.application.context import event, application

from graia.application.protocol.entities.message.elements.internal import Image, Plain, Source
from graia.application.protocol.entities.targets.group import Group

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session.fromUrl("mirai://localhost:8080/ws?authKey=2343142424&qq=208924405")
)

@bcc.receiver("GroupMessage")
async def _(message: MessageChain, group: Group):
    print("?", message.asDisplay())
    if message.asDisplay().startswith("/graia"):
        await app.sendGroupMessage(group, message.asSendable())

print("启动了.")
app.launch()