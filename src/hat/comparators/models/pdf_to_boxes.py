from pathlib import Path

import pdfplumber
from PIL import ImageDraw


from hat.comparators.models.box import Box  # type: ignore
from hat.comparators.models.ptpx import Pt, Px, pt2px  # type: ignore


class PdfToBoxes:
    @staticmethod
    def read(file_path: Path, resolution: int):
        pdf = pdfplumber.open(file_path.as_posix())
        for index, page in enumerate(pdf.pages):
            image = page.to_image(resolution=resolution)

            for char in page.objects["char"]:
                box: Box[Px] = Box(
                    x=pt2px(Pt(char["x0"]), resolution),
                    y=Px(pt2px(Pt(page.height), resolution) - pt2px(Pt(char["y1"]), resolution)),
                    w=pt2px(Pt(char["width"]), resolution),
                    h=pt2px(Pt(char["height"]), resolution),
                    label=char["text"],
                )
                draw = ImageDraw.Draw(image.original)
                draw.rectangle(
                    [(box.x, box.y), (box.x + box.w, box.y + box.h)],
                    outline="red",
                    width=1,
                )
                fontname = char["fontname"]
                import pdb; pdb.set_trace()
                # Correct box by font name
            image.original.save(f"page-{index}.png")


def main():
    PdfToBoxes.read(Path("/Users/manhdt/Projects/Hat/tests/data/doc1.pdf"), 76)


if __name__ == "__main__":
    main()
