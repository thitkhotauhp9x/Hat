import json
import subprocess
import tempfile
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import NewType

import pdfplumber
from PIL import ImageDraw

from hat.comparators.models.box import Box  # type: ignore
from hat.comparators.models.ptpx import Pt, Px, pt2px  # type: ignore

FontPath = NewType("FontPath", str)
FontName = NewType("FontName", str)


def find_font_path(
    mapping: Mapping[FontPath, FontName], font_name: FontName
) -> Path | None:
    for fp, fn in mapping.items():
        if font_name == fn:
            return Path(fp)
    return None


@lru_cache
def load_font_info(font_dir: Path, fontname: str):
    font_mapping = PdfToBoxes.create_mapping_fontname(font_dir)
    font_path = find_font_path(font_mapping, FontName(fontname))
    assert font_path is not None
    font_info = PdfToBoxes.load_font_info(font_path)
    return font_info


@dataclass
class PdfToBoxes:
    @staticmethod
    def read(file_path: Path, resolution: int, page_index: int) -> list[Box[Px]]:
        boxes: list[Box[Px]] = []
        pdf = pdfplumber.open(file_path.as_posix())
        page = pdf.pages[page_index]
        image = page.to_image(resolution=resolution)

        for char in page.objects["char"]:
            box: Box[Px] = Box(
                x=pt2px(Pt(char["x0"]), resolution),
                y=Px(
                    pt2px(Pt(page.height), resolution)
                    - pt2px(Pt(char["y1"]), resolution)
                ),
                w=pt2px(Pt(char["width"]), resolution),
                h=pt2px(Pt(char["height"]), resolution),
                label=char["text"],
                fontname=char["fontname"],
                font_size=char["size"],
            )
            draw = ImageDraw.Draw(image.original)
            PdfToBoxes.draw_box(draw, box)
            boxes.append(box)
        image.original.save(f"page-{page_index}.png")
        return boxes

    @staticmethod
    def debug_boxes(
        file_path: Path, resolution: int, page_index: int, boxes: list[Box[Px]]
    ):
        pdf = pdfplumber.open(file_path.as_posix())
        page = pdf.pages[page_index]
        image = page.to_image(resolution=resolution)
        for box in boxes:
            draw = ImageDraw.Draw(image.original)
            PdfToBoxes.draw_box(draw, box)
        image.original.save(f"page-{page_index}.final.png")

    @staticmethod
    def draw_box(draw, box: Box[Px]):
        draw.rectangle(
            [(box.x, box.y), (box.x + box.w, box.y + box.h)],
            outline="red",
            width=1,
        )

    @staticmethod
    @contextmanager
    def extract_font(pdf_path: Path) -> Generator[Path, None, None]:
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(["mutool", "extract", pdf_path.as_posix()], cwd=temp_dir)
            yield Path(temp_dir)

    @staticmethod
    def create_mapping_fontname(font_dir: Path) -> Mapping[FontPath, FontName]:
        with tempfile.NamedTemporaryFile(suffix=".output.json") as temp_file:
            subprocess.run(
                [
                    "fontforge",
                    "-script",
                    Path("fontforge_scripts/fontname_mapping.py").absolute().as_posix(),
                    "-d",
                    font_dir.as_posix(),
                    "-o",
                    temp_file.name,
                ]
            )
            temp_path = Path(temp_file.name)
            assert temp_path.exists()
            return json.loads(temp_path.read_text())

    @staticmethod
    def load_font_info(font_path: Path):
        with tempfile.NamedTemporaryFile(suffix=".output.json") as temp_file:
            subprocess.run(
                [
                    "fontforge",
                    "-script",
                    Path("fontforge_scripts/font_info.py").absolute().as_posix(),
                    "-f",
                    font_path.as_posix(),
                    "-o",
                    temp_file.name,
                ]
            )
            temp_path = Path(temp_file.name)
            assert temp_path.exists()
            data = json.loads(temp_path.read_text())
            return data

    @staticmethod
    def correct(pdf_path: Path, resolution: int):
        boxes = PdfToBoxes.read(pdf_path, resolution, 0)

        with PdfToBoxes.extract_font(pdf_path) as font_dir:
            for box in boxes:
                font_info = load_font_info(font_dir, box.fontname)
                for char in font_info["chars"]:
                    label = char["char"]
                    if label == box.label:
                        x_min = char["box"]["x_min"]
                        y_min = char["box"]["y_min"]
                        x_max = char["box"]["x_max"]
                        y_max = char["box"]["y_max"]

                        x_min_px = em2px(
                            x_min, box.font_size, resolution, font_info["em"]
                        )
                        y_min_px = em2px(
                            y_min, box.font_size, resolution, font_info["em"]
                        )
                        x_max_px = em2px(
                            x_max, box.font_size, resolution, font_info["em"]
                        )
                        y_max_px = em2px(
                            y_max, box.font_size, resolution, font_info["em"]
                        )

                        width = x_max_px - x_min_px
                        height = y_max_px - y_min_px
                        x = box.x + x_min_px
                        y = box.y + (
                            em2px(
                                font_info["ascent"],
                                box.font_size,
                                resolution,
                                font_info["em"],
                            )
                            - y_max_px
                        )

                        box.x = x
                        box.y = y
                        box.w = width
                        box.h = height

        PdfToBoxes.debug_boxes(pdf_path, resolution, 0, boxes)


def em2px(em, fs, dpi, em_size) -> float:
    return em * fs * dpi / (em_size * 72)


def main():
    PdfToBoxes().correct(Path("/tests/data/doc1.pdf"), 300)


if __name__ == "__main__":
    main()
