import pytest
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from hat.formatters.format import Format


def ask_identity(context: str) -> str:
    return f"""Who are you in this context?

> {context}"""


def ask(context: str):
    pass


@pytest.mark.parametrize(
    "context",
    [
        "Create a prompt template to assert the output of openai is correct with conditions"
    ],
)
@pytest.mark.asyncio
async def test_ask(context: str) -> None:
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    response = await chat_model.ainvoke(
        [
            HumanMessage(
                content=f"""
    Who are you in this context?
    {Format(context):> }
    """
            )
        ]
    )
    print(response.content)


def test_format() -> None:
    assert f"{Format('hello world'):> }" == "> hello world"
