import sys
sys.path.append("..")
from datetime import datetime
from fastapi import APIRouter

from crypto_tracker.daos.portfolios_dao import PortfoliosDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import Portfolio
from crypto_tracker.api.models.pydantic_models.models import PortfolioSchema

DB_URI = get_settings().db_uri

portfolios_router = APIRouter(
    prefix="/portfolios",
)

#CRUD for "portfolio" table
@portfolios_router.get("/")
def get_portfolios():
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolios = portfolio_dao.get_all_portfolios()
    return portfolios



@portfolios_router.get("/{id}")
def get_portfolio(portfolio_id: int):
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolio = portfolio_dao.get_portfolio_by_id(portfolio_id)
    return portfolio


@portfolios_router.post("/")
def add_portfolio(portfolio: PortfolioSchema):
    portfolio_for_insert = Portfolio(user_id=portfolio.user_id, name=portfolio.name, created_at=datetime.now())
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolio = portfolio_dao.create_portfolio(portfolio_for_insert)
    return portfolio


@portfolios_router.patch("/{id}")
def patch_portfolio(portfolio_id: int, updated_portfolio: PortfolioSchema):
    portfolios_dao = PortfoliosDAO(uri=DB_URI)
    coin_to_update = portfolios_dao.patch_portfolio(portfolio_id, updated_portfolio.dict())
    return coin_to_update


@portfolios_router.delete("/{id}")
def delete_portfolio(portfolio_id: int):
    portfolios_dao = PortfoliosDAO(uri=DB_URI)
    portfolio_for_delete = portfolios_dao.get_portfolio_by_id(portfolio_id)
    obj_to_delete = portfolios_dao.delete_portfolio(portfolio_for_delete)
    return obj_to_delete
