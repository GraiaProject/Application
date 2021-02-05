from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.application.message.chain import MessageChain


class MessageChainCatcher(BaseDispatcher):
    @staticmethod
    async def catch(interface: "DispatcherInterface"):
        if interface.annotation is MessageChain:
            return interface.event.messageChain
