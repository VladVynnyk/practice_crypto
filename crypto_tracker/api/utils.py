import time
from functools import wraps
from typing import TypeVar
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from crypto_tracker.config.database import User


# Function for converting SQLAlchemy row to dict
def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# Function for updating values in objects from sqlAlchemy
TModelType = TypeVar("TModelType")


# def update_and_convert_object(model_instance: TModelType, updated_object: dict[str, any]) -> TModelType | None:
#     instance = model_instance
#     instance_for_convert = model_instance.fetchone()
#     for field_name, new_value in updated_object.items():
#         setattr(instance_for_convert, field_name, new_value)
#     print(instance_for_convert)
#     return instance_for_convert
#
#
# def update_row(row, update_dict):
#     for key, value in update_dict.items():
#         setattr(row, key, value)
#         flag_modified(row, key)


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

        # print("count: ", count_of_calls)
        # print("cache: ", cache_dict)

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

        # print("count: ", count_of_calls)
        # print("cache: ", cache_dict)
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
