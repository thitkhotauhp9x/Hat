import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

from hat.anki_flashcard_generator.anki_media_client import AnkiMediaClient
from hat.anki_flashcard_generator.anki_note_client import AnkiNoteClient
from hat.anki_flashcard_generator.ldoce_client import LDOCEClient


class AutoFlashcardGenerator:
    def __init__(self, word: str) -> None:
        self._word = word

    def generate(self) -> None:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        client = LDOCEClient()
        anki_media_client = AnkiMediaClient()
        anki_note_client = AnkiNoteClient()

        for item in client.get_examples(self._word):
            print(item)
            try:
                url = item["audio"]
                file_path = Path(Path(urlparse(url).path).name)

                with open(file_path.as_posix(), "wb") as f:
                    res = session.get(url, timeout=12)
                    res.raise_for_status()
                    f.write(res.content)
                text = item["text"]

                anki_media_client.store_media_file(file_path)

                note_id = anki_note_client.add_note(
                    front=f"[sound:{file_path.as_posix()}]",
                    back=text,
                    deck_name="Default",
                    tags=["vocab", "audio"],
                )
                file_path.unlink()
                print(note_id)
            except Exception as e:
                print(e, file=sys.stderr)