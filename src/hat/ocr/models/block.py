from hat.ocr.models.base_element import BaseElement
from hat.ocr.models.paragraph import Paragraph


class Block(BaseElement):
    paragraphs: list[Paragraph]
