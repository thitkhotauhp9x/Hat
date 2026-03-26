from langchain_core.output_parsers import BaseOutputParser
from markdown_it import MarkdownIt
from typing_extensions import override


MERMAID_OUTPUT_PARSER_TEMPLATE = """\
The output must be a Markdown code block using the "mermaid" language.

Format:
```mermaid
[Your mermaid diagram here]
```
"""


class MermaidOutputParser(BaseOutputParser):
    def __init__(self, index: int = -1) -> None:
        super().__init__()
        self._index: int = index

    def parse(self, text: str) -> str | None:
        markdown = MarkdownIt()
        tokens = markdown.parse(text)
        code_blocks = [
            tok.content
            for tok in tokens
            if tok.type == "fence" and tok.info.strip() == "mermaid"
        ]

        return code_blocks[self._index] if code_blocks else None

    @override
    def get_format_instructions(self) -> str:
        return MERMAID_OUTPUT_PARSER_TEMPLATE
