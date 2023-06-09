from functools import wraps
from typing import TypeVar


# Function for converting SQLAlchemy row to dict
def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# Function for updating values in objects from sqlAlchemy
TModelType = TypeVar("TModelType")


# Decorator for cashing objects

def cache(function: callable) -> callable:
    cache_dict = {}
    count_of_calls = 0
    print("Cache: ", cache_dict)

    @wraps(function)
    def wrapper(*args):
        nonlocal count_of_calls
        count_of_calls += 1
        print(cache_dict)
        if count_of_calls >= 5:
            cache_dict.clear()
            count_of_calls = 0
        if args in cache_dict:
            return cache_dict[args]
        else:
            result = function(*args)
            cache_dict[args] = result
            print("result: ", result)
            return result

    return wrapper


def cache_first_n_calls(n):
    def decorator(func):
        cache = {}
        calls = 0

        def wrapper(*args, **kwargs):
            nonlocal calls

            if calls < n:
                calls += 1
                result = func(*args, **kwargs)
                cache[args] = result
                return result
            else:
                calls = 0
                cache.clear()
                return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_first_n_calls_v2(n: int):
    def decorator(function: callable) -> callable:
        cache_dict = {}
        count_of_calls = 0

        def wrapper(*args):
            nonlocal count_of_calls
            print("count: ", count_of_calls)
            print("cache: ", cache_dict)
            count_of_calls += 1
            if count_of_calls >= n:
                cache_dict.clear()
                count_of_calls = 0
            if args in cache_dict:
                return cache_dict[args]
            else:
                result = function(*args)
                cache_dict[args] = result
                return result

        return wrapper

    return decorator


def cache_first_n_calls_v3(n: int):
    def decorator(function: callable) -> callable:
        cache_dict = {}
        count_of_calls = 0

        @wraps(function)
        def wrapper(*args):
            nonlocal count_of_calls
            print("count: ", count_of_calls)
            print("cache: ", cache_dict)
            count_of_calls += 1
            if count_of_calls >= n:
                cache_dict.clear()
                count_of_calls = 0
            if args in cache_dict:
                return cache_dict[args]
            else:
                result = function(*args)
                cache_dict[args] = result
                return result

        return wrapper

    return decorator


def cache_response(func):
    """
    Decorator that caches the response of a FastAPI async function.

    Example:
    ```
        app = FastAPI()

        @app.get("/")
        @cache_response
        async def example():
            return {"message": "Hello World"}
    ```
    """
    response = []
    count_of_calls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count_of_calls
        count_of_calls+=1
        nonlocal response
        count_of_calls_divided = count_of_calls % 5

        # if count_of_calls_divided != 0:
        # if count_of_calls <= 5:
        if not response:
            response = func(*args, **kwargs)
            print("Saved")
        return response
        # else:
        #     response.clear()
        #     print("List cleared")
    return wrapper