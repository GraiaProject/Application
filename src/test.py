from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.protocol import UploadMethods
from graia.application.protocol.entities import message
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio

from graia.application.protocol.entities.message.elements.internal import Image, Plain, At
from graia.application.protocol.entities.targets.friend import Friend
from graia.application.protocol.entities.targets.group import Group, Member

from devtools import debug

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
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    if message.asDisplay().startswith("At"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id)
        ]))

app.launch_blocking()