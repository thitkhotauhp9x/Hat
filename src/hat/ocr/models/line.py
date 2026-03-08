from hat.ocr.models.base_element import BaseElement
from hat.ocr.models.word import Word


class Line(BaseElement):
    words: list[Word]
