import logging
from contextlib import ContextDecorator, ExitStack
from typing import Any

from openai.resources.chat import Completions, AsyncCompletions
from rich.console import Console
from rich.logging import RichHandler
from rich.json import JSON

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.setLevel(logging.INFO)

create = getattr(Completions, "create")
acreate = getattr(AsyncCompletions, "create")


def mock_method(obj, attr, side_effect):
    from unittest.mock import patch

    return patch.object(obj, attr, side_effect=side_effect, autospec=True)


class log_completion_creation(ContextDecorator):
    def __enter__(self):
        self._stack = ExitStack[Any]()
        self._stack.enter_context(
            mock_method(AsyncCompletions, "create", self._acreate)
        )
        self._stack.enter_context(mock_method(Completions, "create", self._create))
        return self

    @staticmethod
    def _create(*args, **kwargs):
        console = Console(force_terminal=True)
        console.print(JSON.from_data(kwargs))
        result = create(*args, **kwargs)
        console.print(JSON.from_data(result.parse().model_dump(exclude_none=True)))
        return result

    @staticmethod
    async def _acreate(*args, **kwargs):
        console = Console(force_terminal=True)
        console.print(JSON.from_data(kwargs))
        result = await acreate(*args, **kwargs)
        console.print(JSON.from_data(result.parse().model_dump(exclude_none=True)))
        return result

    def __exit__(self, *exc):
        self._stack.close()
        return False
