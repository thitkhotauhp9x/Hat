import hashlib
import pickle
import shelve
from contextlib import contextmanager
from logging import getLogger

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.outputs import LLMResult
from langchain_openai import ChatOpenAI
from pydantic import TypeAdapter
from pytest import MonkeyPatch

logger = getLogger(__name__)


@contextmanager
def mock_generate_from_base_chat_model():
    monkeypatch = MonkeyPatch()
    generate_from_base_chat_model = BaseChatModel.generate

    def generate(self, messages: list[list[BaseMessage]], *args, **kwargs) -> LLMResult:
        dumped_message = TypeAdapter(list[list[BaseMessage]]).dump_python(messages)

        key: str = hashlib.sha256(pickle.dumps((dumped_message,))).hexdigest()

        with shelve.open("data.db") as db:
            if key not in db.keys():
                db[key] = generate_from_base_chat_model(self, messages, *args, **kwargs)
            else:
                logger.warning("Using cached data for a request to OpenAI.")
            return db[key]

    monkeypatch.setattr(BaseChatModel, "generate", generate)
    yield monkeypatch


def main():
    with mock_generate_from_base_chat_model():
        chat_model = ChatOpenAI(model="gpt-4o-mini")
        response = chat_model.invoke([HumanMessage(content="hello")])
        print(response)


if __name__ == "__main__":
    main()
