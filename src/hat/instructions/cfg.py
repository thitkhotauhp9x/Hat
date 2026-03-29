from dataclasses import dataclass

from hat.instructions.base_instruction import BaseInstruction


CFG_TEMPLATE = """
Xây dựng đồ thị luồng điều khiển cho đoạn code sau:

```{lang}
{code}
```
Output dưới dạng mermaid flowchart
"""


@dataclass
class CFG(BaseInstruction):
    code: str
    lang: str

    def get_instruction(self) -> str:
        return CFG_TEMPLATE.format(lang=self.lang, code=self.code)

def trans_set():
    code ="""
def foo(a: int, b: int, c: int, d: int) -> float:
    if a == 0:
        return 0.0

    x = 0
    if (a == b) or (c == d):
        x = 1

    e = 1 / x
    return float(e)
"""
    lang = "python"
    cfg = CFG(code=code, lang=lang)

# input, output
