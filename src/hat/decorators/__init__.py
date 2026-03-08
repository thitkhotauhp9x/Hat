import functools
from typing import Callable

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

CHAT_MODEL = ChatOpenAI(model="gpt-4o-mini")

ASK = CHAT_MODEL | StrOutputParser()


def human_prompt[**P](func: Callable[P, str]) -> Callable[P, str]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return ASK.invoke([HumanMessage(content=func(*args, **kwargs))])

    return wrapper


def ai_prompt[**P](func: Callable[P, str]) -> Callable[P, str]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return ASK.invoke([AIMessage(content=func(*args, **kwargs))])

    return wrapper
