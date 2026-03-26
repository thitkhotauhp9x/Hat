import functools
from typing import Callable, Protocol, Generic


def wrap[**P, R, WR](
    wf: Callable[[R], WR],
) -> Callable[[Callable[P, R]], Callable[P, WR]]:
    def decorator(func: Callable[P, R]) -> Callable[P, WR]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> WR:
            return wf(func(*args, **kwargs))

        return wrapper

    return decorator

class Fn[**P](Protocol):
    def __call__(self, func: Callable[P, str]) -> Callable[P, str]:
        pass


def human_query[**P]() -> Fn[P]:
    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return func(*args, **kwargs)
        return wrapper
    return decorator


@human_query()
def query() -> str:
    return "Hello"
