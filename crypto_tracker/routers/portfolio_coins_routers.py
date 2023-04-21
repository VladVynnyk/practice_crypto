import sys
sys.path.append("..")
import datetime
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.daos.users_dao import UsersDAO
# from .daos.users_dao import UsersDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import PortfolioCoin
from crypto_tracker.api.models.pydantic_models.models import PortfolioCoinSchema

Db_uri = get_settings().db_uri

portfolio_coins_router = APIRouter(
    prefix="/portfolio-coins",
)

#CRUD operations for "PortfolioCoin" table
#Url for this routes must be like this: "/portfolios/{id}/coins{id}"
@portfolio_coins_router.get("/")
def get_portfolio_coins():
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        portfolioCoins = session.query(PortfolioCoin).all()
        return portfolioCoins

@portfolio_coins_router.get("/{id}")
def get_portfolio_coin(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        portfolioCoin = session.query(PortfolioCoin).where(PortfolioCoin.id == id).first()
        return portfolioCoin


@portfolio_coins_router.post("/")
def add_portfolio_coin(portfolioCoin: PortfolioCoinSchema):
    portfolioCoin_for_insert = PortfolioCoin(portfolio_id=portfolioCoin.portfolio_id, coin_id=portfolioCoin.coin_id,
                                             amount=portfolioCoin.amount, created_at=portfolioCoin.created_at)
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.add(portfolioCoin_for_insert)
        session.commit()
    return portfolioCoin

@portfolio_coins_router.patch("/{id}")
def patch_portfolio_coin(id: int, portfolioCoin: PortfolioCoinSchema):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.query(PortfolioCoin).where(PortfolioCoin.id == id).update(portfolioCoin.dict())
        session.commit()
    return portfolioCoin

@portfolio_coins_router.delete("/{id}")
def delete_portfolio_coin(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        query = session.query(PortfolioCoin).where(PortfolioCoin.id==id)
        portfolio_coin = query.first()
        if not portfolio_coin:
            return {"message": "PortfolioCoin not found"}
        session.delete(portfolio_coin)
        session.commit()
    return {"message": "PortfolioCoin deleted"}