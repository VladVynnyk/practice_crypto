import sys
import time

sys.path.append("..")
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.config.settings import get_settings
from crypto_tracker.daos import CoinsDAO

#It's temporary imports
from crypto_tracker.config.database import Coin
from crypto_tracker.api.models.pydantic_models.models import CoinSchema
from crypto_tracker.api.utils import cache, cache_first_n_calls

db_uri = get_settings().db_uri

coins_router = APIRouter(
    prefix="/coins",
)

#CRUD for "coin" table
@coins_router.post("/")
def add_coin(coin: CoinSchema):
    coin_for_insert = Coin(ticker=coin.ticker, fullName=coin.fullName)
    coins_dao = CoinsDAO(uri=db_uri)
    created_coin = coins_dao.create_coin(coin_for_insert)
    return created_coin

@cache_first_n_calls(5)
@coins_router.get("/")
def get_coins():
    coins_dao = CoinsDAO(uri=db_uri)
    coins = coins_dao.get_all_coins()
    # print("Coins: ", coins)
    return coins

@coins_router.get("/{id}")
def get_coin(id: int):
    coins_dao = CoinsDAO(uri=db_uri)
    coin = coins_dao.get_coin_by_id(id)
    # print("COIN: ", coin)
    return coin


@coins_router.patch("/{id}")
def update_coin(coin_id: int, updated_coin: CoinSchema):
    coins_dao = CoinsDAO(uri=db_uri)
    coin_to_update = coins_dao.patch_coin(coin_id, updated_coin.dict())
    return coin_to_update

@coins_router.delete("/{id}")
def delete_coin(coin_id: int):
    coins_dao = CoinsDAO(uri=db_uri)
    coin_for_delete = coins_dao.get_coin_for_operation(coin_id)
    # print("Coin for delete: ", coin_for_delete[0].ticker)
    coin_to_delete = coins_dao.delete_coin(coin_for_delete[0])
    return coin_to_delete