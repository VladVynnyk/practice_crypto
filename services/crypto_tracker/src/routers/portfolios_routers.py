import sys

# sys.path.append("../..")
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from services.crypto_tracker.src.daos.portfolios_dao import PortfoliosDAO
from services.crypto_tracker.src.settings import get_settings

# It's will be temporary imports
from services.crypto_tracker.src.database import Portfolio
from services.crypto_tracker.src.models import PortfolioSchema

from services.crypto_tracker.src.middleware import auth


DB_URI = get_settings().db_uri

portfolios_router = APIRouter(
    prefix="/portfolios",
)


# CRUD for "portfolio" table
@portfolios_router.get("/")
def get_portfolios(api_key: APIKey = Depends(auth.get_api_key)):
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolios = portfolio_dao.get_all_portfolios()
    return portfolios, {"api_key": api_key}


@portfolios_router.get("/{id}")
def get_portfolio(portfolio_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolio = portfolio_dao.get_portfolio_by_id(portfolio_id)

    response = {"portfolio_id": portfolio[0].id, "user_id": portfolio[0].user_id, "name": portfolio[0].name}
    return response


@portfolios_router.get("/user/{id}")
def get_portfolios_by_user(user_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolios = portfolio_dao.get_portfolio_by_user_id(user_id)
    return portfolios


@portfolios_router.post("/")
def add_portfolio(portfolio: PortfolioSchema, api_key: APIKey = Depends(auth.get_api_key)):
    portfolio_for_insert = Portfolio(user_id=portfolio.user_id, name=portfolio.name, created_at=datetime.now())
    portfolio_dao = PortfoliosDAO(uri=DB_URI)
    portfolio = portfolio_dao.create_portfolio(portfolio_for_insert)
    return portfolio


@portfolios_router.patch("/{id}")
def patch_portfolio(portfolio_id: int, updated_portfolio: PortfolioSchema, api_key: APIKey = Depends(auth.get_api_key)):
    portfolios_dao = PortfoliosDAO(uri=DB_URI)
    coin_to_update = portfolios_dao.patch_portfolio(portfolio_id, updated_portfolio.dict())
    return coin_to_update


@portfolios_router.delete("/{id}")
def delete_portfolio(portfolio_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    portfolios_dao = PortfoliosDAO(uri=DB_URI)
    portfolio_for_delete = portfolios_dao.get_portfolio_by_id(portfolio_id)
    obj_to_delete = portfolios_dao.delete_portfolio(portfolio_for_delete)
    return obj_to_delete
