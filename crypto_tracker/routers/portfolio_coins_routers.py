import sys
sys.path.append("..")
from fastapi import APIRouter

from crypto_tracker.daos.portfolio_coins_dao import PortfolioCoinsDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import PortfolioCoin
from crypto_tracker.api.models.pydantic_models.models import PortfolioCoinSchema

DB_URI = get_settings().db_uri

portfolio_coins_router = APIRouter(
    prefix="/portfolio-coins",
)

#CRUD operations for "PortfolioCoin" table
#Url for this routes must be like this: "/portfolios/{id}/coins{id}"
@portfolio_coins_router.get("/")
def get_portfolio_coins():
    portfolio_coins_dao = PortfolioCoinsDAO(uri=DB_URI)
    portfolio_coins = portfolio_coins_dao.get_all_portfolio_coins()
    return portfolio_coins

@portfolio_coins_router.get("/{id}")
def get_portfolio_coin(portfolio_coin_id: int):
    portfolio_coins_dao = PortfolioCoinsDAO(uri=DB_URI)
    portfolio_coin = portfolio_coins_dao.get_portfolio_coin_by_id(portfolio_coin_id)
    return portfolio_coin



@portfolio_coins_router.post("/")
def add_portfolio_coin(portfolio_coin: PortfolioCoinSchema):
    portfolioCoin_for_insert = PortfolioCoin(portfolio_id=portfolio_coin.portfolio_id, coin_id=portfolio_coin.coin_id,
                                             amount=portfolio_coin.amount, created_at=portfolio_coin.created_at)
    portfolio_coins_dao = PortfolioCoinsDAO(uri=DB_URI)
    inserted_portfolio_coin = portfolio_coins_dao.create_portfolio_coin(portfolioCoin_for_insert)
    return inserted_portfolio_coin

@portfolio_coins_router.patch("/{id}")
def patch_portfolio_coin(portfolio_coin_id: int, updated_portfolio_coin: PortfolioCoinSchema):
    portfolio_coins_dao = PortfolioCoinsDAO(uri=DB_URI)
    portfolio_coin_to_update = portfolio_coins_dao.patch_portfolio_coin(portfolio_coin_id, updated_portfolio_coin.dict())
    return portfolio_coin_to_update



@portfolio_coins_router.delete("/{id}")
def delete_portfolio_coin(portfolio_coin_id: int):
    portfolio_coins_dao = PortfolioCoinsDAO(uri=DB_URI)
    portfolio_for_delete = portfolio_coins_dao.get_portfolio_coin_by_id(portfolio_coin_id)
    obj_to_delete = portfolio_coins_dao.delete_portfolio_coin(portfolio_for_delete)
    return obj_to_delete
