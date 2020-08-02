import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.session import Session
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member

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
    print(group.id, member.id)

app.launch_blocking()