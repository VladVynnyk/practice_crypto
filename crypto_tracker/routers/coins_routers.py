import sys
sys.path.append("..")
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.config.settings import get_settings
from crypto_tracker.daos import CoinsDAO

#It's temporary imports
from crypto_tracker.config.database import Coin
from crypto_tracker.api.models.pydantic_models.models import CoinSchema


db_uri = get_settings().db_uri

coins_router = APIRouter(
    prefix="/coins",
)

#CRUD for "coin" table
@coins_router.post("/")
def add_coin(coin: CoinSchema):
    coin_for_insert = Coin(ticker=coin.ticker, fullName=coin.fullName)

    Session = scoped_session(
        sessionmaker(bind=create_engine(db_uri)))
    with Session() as session:
        session.add(coin_for_insert)
        session.commit()
    return coin


@coins_router.get("/")
def get_coins():
    coins_dao = CoinsDAO(uri=db_uri)
    coins = coins_dao.get_all_coins()
    print("Coins: ", coins)
    return coins

@coins_router.get("/{id}")
def get_coin(id: int):
    coins_dao = CoinsDAO(uri=db_uri)
    coin = coins_dao.get_coin_by_id(id)
    print("COIN: ", coin)
    return coin


@coins_router.patch("/{id}")
def update_coin(id, coin: CoinSchema):
    coins_dao = CoinsDAO(uri=db_uri)
    coin = coins_dao.get_coin_by_id(id)
    print("COIN: ", coin)
    return coin


    # coin_for_update = Coin(ticker=coin.ticker, fullName=coin.fullName)

    # Session = scoped_session(
    #     sessionmaker(bind=create_engine(db_uri)))
    # with Session() as session:
    #     session.query(Coin).where(Coin.id == id).update(coin.dict())
    #     session.commit()
    # return coin

@coins_router.delete("/{id}")
def delete_coin(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(db_uri)))
    with Session() as session:
        query = session.query(Coin).where(Coin.id == id)
        coin = query.first()
        if not coin:
            return {"message": "Coin not found"}
        session.delete(coin)
        session.commit()
    return {"message": "Coin deleted"}