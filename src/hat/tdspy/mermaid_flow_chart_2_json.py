from __future__ import annotations
import os
import typing
from enum import Enum
from pathlib import Path
from typing import Literal
import dspy
from dotenv.variables import Literal
from dspy import BootstrapFewShot
from jinja2 import Template
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated

# from hat.tdspy.element import Element

element_registry: set[str] = set()


class ElementType(Enum):
    PROCESS = "Process"
    DECISION = "Decision"
    TERMINATOR = "Terminator"

    pass


class Registry:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        element_registry.add(cls.__name__)


class BaseElement(BaseModel, Registry):
    elementType: ElementType
    elementId: str


class Process(BaseElement):
    elementType: ElementType = ElementType.PROCESS
    name: str


class Decision(BaseElement):
    elementType: ElementType = ElementType.DECISION
    name: str


class Terminator(BaseElement):
    elementType: ElementType = ElementType.TERMINATOR
    name: str


class Flow(BaseModel):
    name: str
    source: str
    target: str


Element: typing.TypeAlias = Process | BaseElement | Decision | Terminator

class FlowChart(BaseModel):
    elements: list[Element]
    flows: list[Flow]


class MermaidFlowChart2Json:

    @staticmethod
    def create_element() -> None:
        template_str = Path("./element.jinja2").read_text(encoding="utf-8")

        template = Template(template_str)

        output = template.render(element_registry=list(element_registry))
        Path("./element.py").write_text(output, encoding="utf-8")


    def train(self):
        self.create_element()
        lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
        dspy.configure(lm=lm)
        lm.inspect_history(n=1)


        class Model(dspy.Signature):
            mermaid = dspy.InputField(desc="A mermaid flow chart")
            json_data = dspy.OutputField(desc=PydanticOutputParser(pydantic_object=FlowChart).get_format_instructions())

        trainset = [
            dspy.Example(
                mermaid="""\
flowchart TD
    A([Start]) --> B[Order burger]
    B --> C{Want fries?}

    C -- Yes --> D[Order fries]
    D --> E{Want drink?}
    C -- No --> E

    E -- Yes --> F[Order drink]
    F --> G[Pay cashier]
    E -- No --> G

    G --> H([End])\
""",
                json_data=FlowChart(
                    elements=[
                        Terminator(name="Start", elementId="start"),
                        Process(name="Order burger", elementId="orderBurger"),
                        Decision(name="Want fries?", elementId="wantFries"),
                        Process(name="Order drink", elementId="orderDrink"),
                        Process(name="Order fires", elementId="orderFires"),
                        Decision(name="Want drink?", elementId="wantDrink"),
                        Process(name="Pay cashier", elementId="payCashier"),
                        Terminator(name="End", elementId="end"),
                    ],
                    flows=[
                        Flow(name="", source="start", target="orderBurger"),
                        Flow(name="", source="orderBurger", target="wantFries"),
                        Flow(name="Yes", source="wantFries", target="orderFires"),
                        Flow(name="No", source="wantFries", target="wantDrink"),
                        Flow(name="Yes", source="wantDrink", target="orderDrink"),
                        Flow(name="No", source="wantDrink", target="payCashier"),
                        Flow(name="", source="payCashier", target="end"),
                    ],
                ).model_dump_json(indent=2),
            ).with_inputs("mermaid"),
        ]

        class ModelClassifier(dspy.Module):
            def __init__(self):
                super().__init__()
                self.prog = dspy.ChainOfThought(Model)

            def forward(self, mermaid: str):
                return self.prog(mermaid=mermaid)

        def validate_context(example, pred, trace=None):
            # import pdb; pdb.set_trace()
            return example.json_data.lower() == pred.json_data.lower()

        optimizer = BootstrapFewShot(metric=validate_context)

        compiled_classifier = optimizer.compile(
            ModelClassifier(), trainset=trainset
        )

        result = compiled_classifier(mermaid="""\
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]\
""")
        import pdb; pdb.set_trace()
        pass

if __name__ == "__main__":
    MermaidFlowChart2Json().train()
