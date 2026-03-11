from typing import NewType

Px = NewType("Px", float)
Pt = NewType("Pt", float)


def px2pt(px: Px, dpi: float) -> Pt:
    return Pt(px * 72 / dpi)


def pt2px(pt: Pt, dpi: float) -> Px:
    return Px(pt * dpi / 72)
