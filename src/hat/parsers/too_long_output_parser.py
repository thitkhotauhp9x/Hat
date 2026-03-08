from typing import Mapping, Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.output_parsers import (
    StrOutputParser,
)
from langchain_core.messages import HumanMessage


def parse(
    chat_model: BaseChatModel,
    messages: list[BaseMessage],
    message: AIMessage,
    times: int = 2,
) -> list[AIMessage]:
    data = [message]

    output_parser = StrOutputParser()

    while not output_parser.invoke(message).strip().lower() == "end" and times > 0:
        messages.append(HumanMessage(content="continue"))
        response = chat_model.invoke(messages)
        data.extend(parse(chat_model, messages, response, times - 1))

    return data
