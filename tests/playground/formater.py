import json
import urllib.parse
from collections import UserString
from enum import StrEnum
from typing import Mapping, Callable
import shlex
from xml.etree import ElementTree


class Quote(StrEnum):
    URL = "url"
    SH = "sh"


MAPPING_QUOTE_FN: Mapping[Quote, Callable[[str], str]] = {
    Quote.URL: urllib.parse.quote,
    Quote.SH: shlex.quote,
}


class StrFormatter(UserString):
    def quote(self, type_quote: Quote) -> str:
        return MAPPING_QUOTE_FN[type_quote](self.data)

    def block_code(self, language: str = "") -> str:
        return f"""{language}
```
{self.data}
```
"""

    def to_xml(self, tag: str) -> str:
        root = ElementTree.Element(tag)
        root.text = self.data
        return ElementTree.tostring(root, encoding="unicode")

    def to_json(self, key: str) -> str:
        return json.dumps({key: self.data}, indent=2)


a = StrFormatter("a?<>bc").to_xml("user_query")
print(a)
