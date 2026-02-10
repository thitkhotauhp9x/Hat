import logging
import subprocess
import uuid
from inspect import signature
from pathlib import Path
from typing import Literal

import pytest
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from langchain_openai import ChatOpenAI
from openai.resources.chat import AsyncCompletions, Completions
from pydantic import BaseModel
from pytest import MonkeyPatch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
formatter = logging.Formatter(
    "%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@pytest.fixture()
def chat_model() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini")


def get_argument_value(attr, func, *args, **kwargs):
    sig = signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments.get(attr)


def _log_sync_request_to_openai(monkeypatch: MonkeyPatch):
    func = Completions.create

    def wrap_request(*args, **kwargs):
        uid = uuid.uuid4()

        for line in yaml.dump(kwargs, allow_unicode=True).splitlines():
            logger.debug("Request  [%s] %s", uid, line)

        response = func(*args, **kwargs)

        for line in yaml.dump(response.parse(), allow_unicode=True).splitlines():
            logger.debug("Response [%s] %s", uid, line)

        return response

    monkeypatch.setattr(Completions, "create", wrap_request)


def _log_async_request_to_openai(monkeypatch: MonkeyPatch):
    func = AsyncCompletions.create

    async def wrap_request(*args, **kwargs):
        uid = uuid.uuid4()

        for line in yaml.dump(kwargs, allow_unicode=True).splitlines():
            logger.debug("Request  [%s] %s", uid, line)

        response = await func(*args, **kwargs)

        for line in yaml.dump(response.parse(), allow_unicode=True).splitlines():
            logger.debug("Response [%s] %s", uid, line)

        return response

    monkeypatch.setattr(AsyncCompletions, "create", wrap_request)


@pytest.fixture()
def log_request_to_openai(monkeypatch: MonkeyPatch):
    _log_sync_request_to_openai(monkeypatch)
    _log_async_request_to_openai(monkeypatch)


@pytest.fixture()
def view_request_to_openai(monkeypatch: MonkeyPatch):
    class Message(BaseModel):
        id: str
        content: str
        role: Literal["user", "system", "assistant"]
        rawData: str

    class Messages(BaseModel):
        messages: list[Message]

    func = Completions.create

    env = Environment(loader=PackageLoader("debugger"), autoescape=select_autoescape())
    template = env.get_template("index.html")

    data = Messages(messages=[])

    def wrapper(*args, **kwargs):
        messages = get_argument_value("messages", func, *args, **kwargs)

        for index, message in enumerate(messages):
            data.messages.append(
                Message(
                    content=message["content"],
                    role=message["role"],
                    id=str(uuid.uuid4()),
                    rawData=yaml.dump(kwargs, allow_unicode=True),
                )
            )

        response = func(*args, **kwargs)

        data.messages.append(
            Message(
                content=response.parse().choices[0].message.content,
                role=response.parse().choices[0].message.role,
                id=str(uuid.uuid4()),
                rawData="",
            )
        )
        Path("output.html").write_text(template.render(data.model_dump()))
        subprocess.Popen(["open", "output.html"])
        return response

    monkeypatch.setattr(Completions, "create", wrapper)
