from __future__ import annotations
from typing import Optional
from . import ExternalElement

class Image(ExternalElement):
    type: str = "Image"
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

    def asSerializationString(self) -> str:
        return f"[mirai:image:{self.imageId}]"

class FlashImage(Image):
    type = "FlashImage"

    def asSerializationString(self) -> str:
        return f"[mirai:flash:{self.imageId}]"