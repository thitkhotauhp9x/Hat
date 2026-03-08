from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai._response import APIResponse


def test_openai_query(chat_model: BaseChatModel, log_request_to_openai) -> None:
    response = chat_model.invoke([HumanMessage(content="Hello you")])
    print(response)
