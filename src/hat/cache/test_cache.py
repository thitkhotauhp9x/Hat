import hashlib
import pickle
import shelve


def test_cache():
    def key_factory(func: Func[[int, int], int], a: int, b: int) -> str:
        return hashlib.sha256().hexdigest()

    with shelve.open("data.db") as db:
        custom_cache = cache(
            db=db,
            encode=pickle.loads,
            decode=pickle.dumps,
            key_factory=key_factory,
        )
