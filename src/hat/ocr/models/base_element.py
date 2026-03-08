from dataclasses import dataclass

from hat.ocr.models.bounding_box import BoundingBox


@dataclass
class BaseElement:
    text: str
    bounding_box: BoundingBox
