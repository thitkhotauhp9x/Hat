import pytest
from langchain_core.messages import HumanMessage

from hat.playground.chat import Chat
from tests.playground.assertion import assert_is_same_content


@pytest.mark.asyncio
async def test_query_by_agent() -> None:
    chat = Chat.model_validate({})
    response = chat.query(
        human_message=HumanMessage(content="Hello"),
    )
    await assert_is_same_content(response, "Hello! How can I assist you today?")
