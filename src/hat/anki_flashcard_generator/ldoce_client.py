import requests
from bs4 import BeautifulSoup
from typing import Dict, List


class LDOCEClient:
    BASE_URL = "https://www.ldoceonline.com/dictionary/"

    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        self.timeout = timeout

    def _fetch_page(self, word: str) -> str:
        url = self.BASE_URL + word
        res = self.session.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.text

    def get_audio(self, word: str) -> Dict[str, List[str]]:
        html = self._fetch_page(word)
        soup = BeautifulSoup(html, "html.parser")

        result = {"uk": [], "us": [], "examples": []}

        for sp in soup.select("span.speaker"):
            mp3 = sp.get("data-src-mp3")
            if not mp3:
                continue

            classes = sp.get("class", [])

            if "brefile" in classes:
                result["uk"].append(mp3)
            elif "amefile" in classes:
                result["us"].append(mp3)
            elif "exafile" in classes:
                result["examples"].append(mp3)

        return result

    def get_first_pronunciation(self, word: str) -> Dict[str, str]:
        """
        Lấy pronunciation đầu tiên (canonical)
        """
        audio = self.get_audio(word)

        return {
            "uk": audio["uk"][0] if audio["uk"] else None,
            "us": audio["us"][0] if audio["us"] else None,
        }

    def download_audio(self, url: str, filename: str):
        res = self.session.get(url, timeout=self.timeout)
        res.raise_for_status()

        with open(filename, "wb") as f:
            f.write(res.content)

    def download_pronunciations(self, word: str, prefix: str = None):
        """
        Download UK + US pronunciation
        """
        prefix = prefix or word
        audio = self.get_first_pronunciation(word)

        if audio["uk"]:
            self.download_audio(audio["uk"], f"{prefix}_uk.mp3")

        if audio["us"]:
            self.download_audio(audio["us"], f"{prefix}_us.mp3")

    def get_examples(self, word: str) -> List[Dict[str, str]]:
        html = self._fetch_page(word)
        soup = BeautifulSoup(html, "html.parser")

        results = []

        for ex in soup.select("span.EXAMPLE"):
            speaker = ex.select_one("span.speaker")
            audio = speaker.get("data-src-mp3") if speaker else None

            text = ex.get_text(strip=True)

            results.append({"text": text, "audio": audio})

        return results
