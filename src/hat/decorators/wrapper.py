import functools
from typing import Callable


def wrap[**P, R, WR](
    wf: Callable[[R], WR],
) -> Callable[[Callable[P, R]], Callable[P, WR]]:
    def decorator(func: Callable[P, R]) -> Callable[P, WR]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> WR:
            return wf(func(*args, **kwargs))

        return wrapper

    return decorator
