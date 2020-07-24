from devtools import debug
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio

from graia.application.protocol.entities.message.elements.internal import Image, Plain

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session.fromUrl("mirai://localhost:8080/ws?authKey=2343142424&qq=208924405")
)

@bcc.receiver("GroupMessage")
def _(message: MessageChain):
    debug(message)

app.launch_with()