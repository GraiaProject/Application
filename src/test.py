from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.protocol import UploadMethods
from graia.application.protocol.entities import message
from graia.application.protocol.entities.message.chain import MessageChain
import asyncio

from graia.application.protocol.entities.message.elements.internal import Image, Plain
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
async def m(app: GraiaMiraiApplication, member: Member, message: MessageChain, group: Group):
    if member.id == 1846913566 and message.asDisplay().startswith("并发图片上传测试"):
        """
        images = await asyncio.gather(
            app.uploadImage(
                open("G:\\绅士图册\\5301c8a785c2545661cbebe04d619d97_big.jpg", "rb").read(),
                UploadMethods.Group, 
                return_external=True
            ),
            app.uploadImage(
                open("G:\\绅士图册\\IMG_289.jpg", "rb").read(),
                UploadMethods.Group,
                return_external=True
            ),
            app.uploadImage(
                open("G:\\绅士图册\\IMG_290.png", "rb").read(),
                UploadMethods.Group,
                return_external=True
            ),
        )"""
        images_chain = MessageChain.create([
            Plain("测试 mirai-api-http #126."),
            Image.fromLocalFile("G:\\绅士图册\\IMG_289.jpg"),
            Image.fromLocalFile("G:\\绅士图册\\5301c8a785c2545661cbebe04d619d97_big.jpg"),
            Image.fromLocalFile("G:\\绅士图册\\IMG_290.png")
        ])
        await app.sendGroupMessage(group, images_chain)

@bcc.receiver("TempMessage")
async def m(message: MessageChain):
    debug(message)

app.launch_blocking()