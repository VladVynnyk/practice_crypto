import sys
sys.path.append("..")
from datetime import datetime
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.daos.users_dao import UsersDAO
# from .daos.users_dao import UsersDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import Portfolio
from crypto_tracker.api.models.pydantic_models.models import PortfolioSchema

Db_uri = get_settings().db_uri

portfolios_router = APIRouter(
    prefix="/portfolios",
)

#CRUD for "portfolio" table
@portfolios_router.get("/")
def get_portfolios():
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        portfolios = session.query(Portfolio).all()
        return portfolios

@portfolios_router.get("/{id}")
def get_portfolio(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        portfolio = session.query(Portfolio).where(Portfolio.id == id).first()
        return portfolio

@portfolios_router.post("/")
def add_portfolio(portfolio: PortfolioSchema):
    portfolio_for_insert = Portfolio(user_id=portfolio.user_id, name=portfolio.name, created_at=datetime.now())

    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.add(portfolio_for_insert)
        session.commit()
    return portfolio

@portfolios_router.patch("/{id}")
def patch_portfolio(id: int, portfolio: PortfolioSchema):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.query(Portfolio).where(Portfolio.id == id).update(portfolio.dict())
        session.commit()
    return portfolio

@portfolios_router.delete("/{id}")
def delete_portfolio(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        query = session.query(Portfolio).where(Portfolio.id == id)
        portfolio = query.first()
        if not portfolio:
            return {"message": "Portfolio not found"}
        session.delete(portfolio)
        session.commit()
    return {"message": "Portfolio deleted"}
