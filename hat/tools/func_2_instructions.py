from typing import Awaitable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from playground.chat import Chat

FUNC_TO_INSTRUCTION_SYS_MSG = """# Identity

* You are an AI assistance

# Instructions

* Convert the function to instructions"""


def convert_func_to_instructions(func: str) -> Awaitable[str]:
    chat = Chat(
        system_message=SystemMessage(content=FUNC_TO_INSTRUCTION_SYS_MSG),
        prompt_messages=[
            HumanMessage(
                content="""\
def add(a, b):
    return a + b\
"""
            ),
            AIMessage(
                content="""\
1. Identify the first number (let's call it 'a').
2. Identify the second number (let's call it 'b').
3. Add 'a' and 'b' together.
4. Return the result of the addition.\
"""
            ),
        ],
    )
    response = chat.query(
        human_message=HumanMessage(content=func),
        output_parser=StrOutputParser(),
    )
    return response
