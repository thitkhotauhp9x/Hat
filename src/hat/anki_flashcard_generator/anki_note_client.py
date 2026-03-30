import requests


class AnkiNoteClient:
    def __init__(self, endpoint: str = "http://localhost:8765"):
        self.endpoint = endpoint

    def _request(self, action: str, params: dict):
        payload = {"action": action, "version": 6, "params": params}

        response = requests.post(self.endpoint, json=payload)
        response.raise_for_status()

        result = response.json()
        if result.get("error"):
            raise Exception(f"Anki error: {result['error']}")

        return result.get("result")

    def add_note(
        self,
        front: str,
        back: str,
        deck_name: str = "Default",
        model_name: str = "Cơ bản",
        tags: list[str] | None = None,
        allow_duplicate: bool = False,
    ) -> int:
        """
        Tạo note mới trong Anki.

        Args:
            front: nội dung Front (vd: [sound:apple.mp3])
            back: nội dung Back (vd: apple)
            deck_name: tên deck
            model_name: loại note (Basic, Basic (and reversed card), ...)
            tags: list tag
            allow_duplicate: cho phép trùng

        Returns:
            note id (int)
        """
        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": {"Mặt trước": front, "Mặt sau": back},
            "options": {"allowDuplicate": allow_duplicate},
            "tags": tags or [],
        }

        return self._request("addNote", {"note": note})
