from pydantic import BaseModel


class BotMessage(BaseModel):
    messageId: int
