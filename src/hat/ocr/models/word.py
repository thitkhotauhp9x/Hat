from hat.ocr.models.base_element import BaseElement
from hat.ocr.models.charactor import Charactor


class Word(BaseElement):
    characters: list[Charactor]
