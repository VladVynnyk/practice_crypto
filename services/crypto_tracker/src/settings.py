import os
from functools import cache

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()

Db_uri = os.environ.get("DB_URI")



class Settings(BaseSettings):
    db_uri: PostgresDsn


@cache
def get_settings() -> Settings():
    return Settings()
