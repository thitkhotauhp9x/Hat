from pathlib import Path

import dspy
from jinja2 import Template


def save(lm: dspy.LM, op: Path) -> None:
    assert op.suffix == ".py"
    last_call = lm.history[-1]
    path = Path(__file__).with_name("langchain.jina2")
    template = Template(path.read_text())
    output = template.render(messages=last_call["messages"])
    op.write_text(output)
