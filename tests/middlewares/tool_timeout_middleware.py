import asyncio
import logging
import time
from typing import Callable, Awaitable

from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command


logger = logging.getLogger(__name__)


class ToolTimeoutMiddleware(AgentMiddleware):

    def __init__(self, tool_names: list[str], end_time: float):
        super().__init__()
        self._tool_names = tool_names
        self._end_time = end_time

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        if request.tool is not None and request.tool.name in self._tool_names:
            timeout = self._end_time - time.monotonic()
            logger.info("Timeout %s", timeout)
            result = await asyncio.wait_for(handler(request), timeout=timeout)
        else:
            result = await handler(request)
        return result
