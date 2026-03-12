from pydantic import BaseModel

from hat.comparators.models.unit import Em


class Box[T](BaseModel):
    x_min: T
    y_min: T
    x_max: T
    y_max: T


class Character[T](BaseModel):
    char: str
    unicode: int
    box: Box[T]


class FontBox[T](BaseModel):
    em: Em
    ascent: Em
    chars: list[Character[T]]
