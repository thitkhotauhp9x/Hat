import contextlib
import uuid
from inspect import signature
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator, Literal

from jinja2 import Environment, PackageLoader, select_autoescape
from openai.resources.chat import Completions
from pydantic import BaseModel
from pytest import MonkeyPatch
from selenium import webdriver


def get_argument_value(attr, func, *args, **kwargs):
    sig = signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments.get(attr)


class Message(BaseModel):
    id: str
    content: str
    role: Literal["user", "system", "assistant"]


class Messages(BaseModel):
    messages: list[Message]


driver = webdriver.Chrome()
env = Environment(loader=PackageLoader("src.debugger"), autoescape=select_autoescape())


@contextlib.contextmanager
def debugger() -> Generator[MonkeyPatch, None, None]:
    import pdb

    pdb.set_trace()
    func = Completions.create

    template = env.get_template("index.html")

    data = Messages(messages=[])

    def wrapper(*args, **kwargs):
        import pdb

        pdb.set_trace()
        messages = get_argument_value("messages", func, *args, **kwargs)

        for index, message in enumerate(messages):
            data.messages.append(
                Message(
                    content=message["content"],
                    role=message["role"],
                    id=str(uuid.uuid4()),
                )
            )

        response = func(*args, **kwargs)

        messages = response.parse().choices[0].message
        data.messages.append(
            Message(
                content=messages.content,
                role=messages.role,
                id=str(uuid.uuid4()),
            )
        )
        with NamedTemporaryFile(suffix=".html") as temp_file:
            import pdb

            pdb.set_trace()
            temp_path = Path(temp_file.name)
            temp_path.write_text(template.render(data.model_dump()))
            driver.get(temp_path.as_uri())

        return response

    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(Completions, "create", wrapper)
    yield monkeypatch
