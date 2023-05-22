import os
from functools import cache

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()

Db_uri = os.environ.get("DB_URI")
API_KEY = os.environ.get("API_KEY")
URL_TO_LOCAL_API = os.environ.get("URL_TO_LOCAL_API")
URL_TO_LOCAL_API_IN_DOCKER = os.environ.get("URL_TO_LOCAL_API_IN_DOCKER")


class Settings(BaseSettings):
    db_uri: PostgresDsn
    api_key: str
    url_to_local_api: str
    url_to_local_api_in_docker: str

@cache
def get_settings() -> Settings():
    return Settings()
