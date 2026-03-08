from abc import ABC, abstractmethod

import pytesseract

from hat.ocr.models.bounding_box import BoundingBox
from hat.ocr.models.word import Word


class Image(ABC):
    pass


class BaseBinarizationImage(ABC):
    @abstractmethod
    def binarize(self) -> Image:
        pass


def get_words(image) -> list[Word]:
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    word_list: list[Word] = []

    for i, word in enumerate(data["text"]):
        if word.strip() != "":
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            word = Word(text=word, bounding_box=BoundingBox(x, y, w, h))
            word_list.append(word)
    return word_list
