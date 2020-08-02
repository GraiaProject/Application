from __future__ import annotations
from typing import Optional
from . import ExternalElement

class Image(ExternalElement):
    type: str = "Image"
    imageId: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

class FlashImage(Image):
    pass