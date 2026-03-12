from typing import NewType

Px = NewType("Px", float)
Pt = NewType("Pt", float)
Em = NewType("Em", float)

FontPath = NewType("FontPath", str)
FontName = NewType("FontName", str)


def px2pt(px: Px, dpi: float) -> Pt:
    return Pt(px * 72 / dpi)


def pt2px(pt: Pt, dpi: float) -> Px:
    return Px(pt * dpi / 72)


def em2px(em: Em, font_size: float, dpi: float, em_size: Em) -> Px:
    return Px(em * font_size * dpi / (em_size * 72))
