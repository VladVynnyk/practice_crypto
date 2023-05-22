from __future__ import annotations
import sys

from services.crypto_tracker.src.middleware import auth

# sys.path.append("../..")

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from services.crypto_tracker.src.settings import get_settings
from services.crypto_tracker.src.daos import CoinsDAO

# It's temporary imports
from services.crypto_tracker.src.database import Coin
from services.crypto_tracker.src.models import CoinSchema
from services.crypto_tracker.src.utils import cache_response

db_uri = get_settings().db_uri

coins_router = APIRouter(
    prefix="/coins",
)


# CRUD for "coin" table
@coins_router.post("/")
def add_coin(coin: CoinSchema, api_key: APIKey = Depends(auth.get_api_key)):
    coin_for_insert = Coin(ticker=coin.ticker, fullName=coin.fullName)
    coins_dao = CoinsDAO(uri=db_uri)
    created_coin = coins_dao.create_coin(coin_for_insert)
    print("coin: ", coin)
    print("created_coin", created_coin)
    return created_coin


@coins_router.get("/")
# @cache_response
def get_coins(api_key: APIKey = Depends(auth.get_api_key)):
    coins_dao = CoinsDAO(uri=db_uri)
    coins = coins_dao.get_all_coins()
    # print("Coins: ", coins)
    return coins


@coins_router.get("/{id}")
# @cache_response
def get_coin(coin_id: int, api_key: APIKey = Depends(auth.get_api_key)) -> CoinSchema:
    coins_dao = CoinsDAO(uri=db_uri)
    coin = coins_dao.get_coin_by_id(coin_id)

    response = {"id": coin[0].id, "ticker": coin[0].ticker, "fullName": coin[0].fullName}
    return response


@coins_router.patch("/{id}")
def update_coin(coin_id: int, updated_coin: CoinSchema, api_key: APIKey = Depends(auth.get_api_key)):
    coins_dao = CoinsDAO(uri=db_uri)
    coin_to_update = coins_dao.patch_coin(coin_id, updated_coin.dict())
    return coin_to_update


@coins_router.delete("/{id}")
def delete_coin(coin_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    coins_dao = CoinsDAO(uri=db_uri)
    coin_for_delete = coins_dao.get_coin_by_id(coin_id)
    print("Coin for delete: ", coin_for_delete)

    coin_to_delete = coins_dao.delete_coin(coin_for_delete)
    return coin_to_delete
