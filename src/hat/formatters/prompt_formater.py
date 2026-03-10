import shlex
import textwrap
import urllib.parse
from collections import UserString
from xml.etree import ElementTree

from hat.formatters.block_code_language import BlockCodeLanguage  # type: ignore


class PromptFormatter(UserString):
    def quote_url(self) -> str:
        return urllib.parse.quote(self.data)

    def quote_sh(self) -> str:
        return shlex.quote(self.data)

    def indent(self, prefix: str) -> str:
        return textwrap.indent(self.data, prefix, predicate=lambda line: True)

    def escape(self) -> str:
        return self.data.encode("unicode_escape").decode()

    def create_block_code(self, lang: BlockCodeLanguage) -> str:
        if __debug__:
            if "```" in self.data:
                raise AssertionError("'```' in content")

        return f"""
```{lang}
{self.data}
```"""

    def create_xml_content(self, tag: str) -> str:
        root = ElementTree.Element(tag)
        root.text = self.data
        return ElementTree.tostring(root, encoding="unicode")
