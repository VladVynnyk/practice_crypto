from __future__ import annotations

import logging

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.database import Portfolio
from services.crypto_tracker.src.models import PortfolioSchema

logger = logging.getLogger(__name__)


class PortfoliosDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = DBClient(uri)

    def get_portfolio_by_id(self, coin_id: int) -> PortfolioSchema | None:
        query = select(Portfolio).where(Portfolio.id == coin_id)
        return self._get_one_portfolio_by_query(query)

    def get_portfolio_by_user_id(self, user_id: int)-> PortfolioSchema | None:
        query = select(Portfolio).where(Portfolio.user_id == user_id)
        return self._get_all_portfolios(query)

    def get_all_portfolios(self) -> PortfolioSchema | None:
        query = select(Portfolio)
        return self._get_all_portfolios(query)

    def create_portfolio(self, coin: Portfolio) -> PortfolioSchema | None:
        return self._db_client.create_object(coin)

    def patch_portfolio_coin(self, portfolio_id: int, updated_portfolio: dict[str, any]) -> PortfolioSchema | None:
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?
        query = update(Portfolio).where(Portfolio.id == portfolio_id).values(user_id=updated_portfolio['user_id'], name=updated_portfolio['name'], created_at=updated_portfolio['created_at']).returning(Portfolio.id, Portfolio.name, Portfolio.user_id, Portfolio.name)
        return self._db_client.update_object(query)

    def delete_portfolio(self, coin: Portfolio) -> PortfolioSchema | None:
        return self._db_client.delete_object(coin)

    def _get_one_portfolio_by_query(self, query: Select) -> PortfolioSchema | None:
        try:
            return self._db_client.select_one_object_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when user id is not a valid UUID
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_portfolios(self, query: Select) -> PortfolioSchema | None:
        try:
            return self._db_client.select_all_objects(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))
