from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser


@dataclass
class SimpleChat:
    base_model: BaseChatModel

    def chat(self, message_content: str) -> str:
        chain = self.base_model | StrOutputParser()

        return chain.invoke(
            [
                HumanMessage(content=message_content),
            ]
        )


def human_query(base_model: BaseChatModel):
    chain = base_model | StrOutputParser()

    def decorator(func):
        def wrapper(*args, **kwargs) -> str:
            message_content = func(*args, **kwargs)
            return chain.invoke([HumanMessage(content=message_content)])

        return wrapper

    return decorator
