import time
from typing import Any

import pytest
from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    ToolRetryMiddleware,
)
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from tests.middlewares.tool_timeout_middleware import ToolTimeoutMiddleware
from tests.tools.add import add
from tests.tools.weather import weather


class AgentInput(BaseModel):
    messages: list[BaseMessage]


@pytest.mark.asyncio
async def test_timeout_middleware() -> None:
    model = ChatOpenAI(model="gpt-4o-mini")

    middleware: list[AgentMiddleware[Any, Any]] = [
        ToolRetryMiddleware(max_retries=0, on_failure="continue"),
        ToolTimeoutMiddleware(tool_names=["add"], end_time=time.monotonic() - 10),
    ]

    agent = create_agent(
        tools=[add, weather],
        model=model,
        middleware=middleware,
        debug=True,
    )

    await agent.ainvoke(
        AgentInput(messages=[HumanMessage(content="The result of 3 and 7")])
    )
