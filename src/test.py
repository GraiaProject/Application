from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio

from graia.application.protocol.entities.message.elements.internal import Plain
from graia.application.protocol.entities.targets.friend import Friend
from graia.application.protocol.entities.targets.group import Member

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",
        authKey="2343142424",
        account=208924405,
        websocket=False
    )
)

@bcc.receiver("GroupMessage")
async def m(app: GraiaMiraiApplication, member: Member):
    print("?")

app.launch_blocking()