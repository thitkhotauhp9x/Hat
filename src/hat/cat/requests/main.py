import argparse

from hat.cat.requests.auto_flashcard_generator import AutoFlashcardGenerator


def main() -> None:
    parser = argparse.ArgumentParser("Create audio flashcard.")
    parser.add_argument(
        "-w", "--word", required=True, type=str
    )

    args = parser.parse_args()

    AutoFlashcardGenerator(word=args.word).generate()


if __name__ == "__main__":
    main()
