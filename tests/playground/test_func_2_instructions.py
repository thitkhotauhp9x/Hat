import pytest
from langchain_core.messages import HumanMessage, SystemMessage

from playground.chat import Chat
from tools.func_2_instructions import convert_func_to_instructions
from tests.playground.assertion import assert_is_same_content


@pytest.mark.asyncio
async def test_func_2_instructions() -> None:
    instructions = await convert_func_to_instructions("""\
def add(a, b):
    return a + b\
""")

    chat = Chat(
        system_message=SystemMessage(
            content=f"""\
# Identity

* You are an AI assistance

# Instructions

{instructions}\
"""
        ),
    )
    response = await chat.query(human_message=HumanMessage(content="a=1, b=2"))
    await assert_is_same_content(response, "The sum of a and b is 3.")
