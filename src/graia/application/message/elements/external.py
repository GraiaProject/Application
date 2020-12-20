from typing import Optional
from . import ExternalElement


class Image(ExternalElement):
    type: str = "Image"
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

    def asSerializationString(self) -> str:
        return f"[mirai:image:{self.imageId}]"


class FlashImage(Image, ExternalElement):
    type = "FlashImage"

    def asSerializationString(self) -> str:
        return f"[mirai:flash:{self.imageId}]"


class Voice(ExternalElement):
    type = "Voice"
    voiceId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

    def asSerializationString(self) -> str:
        return f"[mirai:voice:{self.voiceId}]"
