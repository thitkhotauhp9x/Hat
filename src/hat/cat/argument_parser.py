import argparse
import os
from pathlib import Path

import dspy
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from jinja2 import Template

from dspy.teleprompt import BootstrapFewShot


def validate_context(example, pred, trace=None):
    return example.sentiment.lower() == pred.sentiment.lower()


def main(output_path: Path):
    class Model(dspy.Signature):
        requirement = dspy.InputField()
        output = dspy.OutputField(desc=format_instructions)
        pass

    trainset = [
        dspy.Example(
            requirement="Create a 20 year old student",
            output=...,
        ),
        dspy.Example(
            requirement="Create a student",
            output=Student(name="Lee", old=14).model_dump_json(indent=2),
        ),
    ]
    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.configure(lm=lm)
    predict = dspy.Predict(Model)
    predict.demos = trainset
    optimizer = BootstrapFewShot(metric=None)

    compiled = optimizer.compile(dspy.Predict(Model), trainset=trainset)
    result = compiled(requirement="Create a asian student data.")
    lm.inspect_history(n=1)

    last_call = lm.history[-1]

    path = Path(__file__).with_name("./langchain.jina2")
    template = Template(path.read_text())
    output = template.render(messages=last_call["messages"])
    output_path.write_text(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", default="output.py", help="Write code to a file (.py)"
    )

    args = parser.parse_args()
    main(Path(args.output))
