import argparse
import os
from pathlib import Path
from typing import Annotated

import dspy
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from dspy.teleprompt import BootstrapFewShot

from hat.cat.common import save


def validate_context(example, pred, trace=None):
    return example.sentiment.lower() == pred.sentiment.lower()


class Student(BaseModel):
    name: str
    old: Annotated[int, Field(description="Old, int, > 0")]


class Response(BaseModel):
    reasoning: str
    errorMessage: str


output_parser = PydanticOutputParser(pydantic_object=Student)
format_instructions = output_parser.get_format_instructions()


class Model(dspy.Signature):
    requirement = dspy.InputField()
    output = dspy.OutputField(desc=format_instructions)


trainset = [
    dspy.Example(
        requirement="Create a 20 year old student",
        output=Student(name="John", old=20).model_dump_json(indent=2),
    ).with_inputs("requirement"),
    dspy.Example(
        requirement="Create a student",
        output=Student(name="Lee", old=14).model_dump_json(indent=2),
    ).with_inputs("requirement"),
]


def main(prompt: str, output_path: Path) -> None:
    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.settings.configure(lm=lm, track_usage=True)
    dspy.configure(lm=lm)

    predict = dspy.Predict(Model)
    predict.demos = trainset
    optimizer = BootstrapFewShot(metric=validate_context)

    compiled = optimizer.compile(dspy.Predict(Model), trainset=trainset)
    result = compiled(prompt)
    save(lm, output_path)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", default="output.py", help="Write code to a file (.py)"
    )
    parser.add_argument(
        "-p", "--prompt", help="Prompt",
    )

    args = parser.parse_args()

    main(args.prompt, Path(args.output))
