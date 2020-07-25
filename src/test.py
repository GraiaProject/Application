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
        host="http://localhost:8080",
        authKey="graia-mirai-api-http-authkey",
        account=5234120587,
        websocket=True
    )
)

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain(__root__=[
        Plain("Hello, World!")
    ]))

app.launch()