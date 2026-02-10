import pytest
from data import data_path
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from playground.chat import Chat
from tests.playground.assertion import assert_is_same_content


@pytest.mark.asyncio
async def test_query() -> None:
    chat = Chat()

    response = await chat.query(human_message=HumanMessage(content="Hello"))
    await assert_is_same_content(response, "Hello! How can I assist you today?")


async def test_query_by_agent() -> None:
    chat = Chat()
    response = chat.query_by_agent(
        human_message=HumanMessage(content="Hello"), output_parser=StrOutputParser()
    )
    await assert_is_same_content(response, "Hello! How can I assist you today?")


def test_query_by_agent_with_document(log_request_to_openai) -> None:
    chat = Chat(
        files=[data_path / "info.pdf"],
    )

    response = chat.query_by_agent(
        human_message=HumanMessage(content="Tên của tôi là gì?"),
        output_parser=StrOutputParser(),
    )
