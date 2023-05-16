import sys

from services.coins_fetchers.main import execute_fetchers

sys.path.append("../../..")
from fastapi import APIRouter

from services.crypto_tracker.src.settings import get_settings


DB_URI = get_settings().db_uri

users_router = APIRouter(
    prefix="/fetch",
)

# CRUD for "user" table
@users_router.get("/")
def fetch_info_about_coins_in_portfolio():
    fetchers = execute_fetchers()
    return fetchers

