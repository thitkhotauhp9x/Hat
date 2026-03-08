import shelve
from functools import wraps
from typing import Callable, Protocol


class Func[**P, R](Protocol):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        pass


class CallFunc[**P, R, Key](Protocol):
    def __call__(self, func: Func[P, R], *args: P.args, **kwargs: P.kwargs) -> Key:
        pass


def cache[**Param, Result](
    dbname: str,
    key_factory: CallFunc[Param, Result, str],
    renew: bool = False,
) -> Callable[[Func[Param, Result]], Callable[Param, Result]]:
    def decorator(func: Func[Param, Result]) -> Callable[Param, Result]:
        @wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> Result:
            with shelve.open(dbname) as db:
                key = key_factory(func, *args, **kwargs)
                if key not in db.keys():
                    db[key] = [func(*args, **kwargs)]
                else:
                    if renew:
                        db[key].append(func(*args, **kwargs))
                return db[key][-1]

        return wrapper

    return decorator
