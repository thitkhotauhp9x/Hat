import base64
import requests
from pathlib import Path


class AnkiMediaClient:
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

    def store_media_file(
        self, file_path: str | Path, filename: str | None = None
    ) -> str:
        """
        Upload file vào Anki media.

        Args:
            file_path: đường dẫn file local (.mp3)
            filename: tên lưu trong Anki (optional)

        Returns:
            filename đã lưu trong Anki
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if filename is None:
            filename = file_path.name

        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        self._request("storeMediaFile", {"filename": filename, "data": encoded})

        return filename
