from pydantic import BaseModel


class Box(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class Character(BaseModel):
    char: str
    unicode: str
    box: Box


class Font(BaseModel):
    em: float
    chars: list[Character]
