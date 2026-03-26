import argparse
from pathlib import Path

from hat.pdf_to_boxes.pdf_to_boxes import PdfToBoxes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="PDF file")
    parser.add_argument("-r", "--resolution", help="Resolution")

    args = parser.parse_args()
    pdf_file_path = Path(args.file)
    resolution = int(args.resolution)
    pdf_to_boxes = PdfToBoxes()
    pdf_to_boxes.convert(pdf_file_path, resolution=resolution)


if __name__ == "__main__":
    main()
