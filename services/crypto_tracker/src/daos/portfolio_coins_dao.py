from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.database import PortfolioCoin
from services.crypto_tracker.src.models import PortfolioCoinSchema

logger = logging.getLogger(__name__)


class PortfolioCoinsDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = DBClient(uri)

    def get_portfolio_coin_by_id(self, portfolio_coin_id: int) -> PortfolioCoinSchema | None:
        query = select(PortfolioCoin).where(PortfolioCoin.id == portfolio_coin_id)
        return self._get_one_portfolio_coin_by_query(query)

    def get_portfolio_coins_by_portfolio_id(self, portfolio_id: int) -> PortfolioCoinSchema | None:
        query = select(PortfolioCoin).where(PortfolioCoin.portfolio_id == portfolio_id)
        return self._get_all_portfolio_coins(query)

    def get_all_portfolio_coins(self) -> PortfolioCoinSchema | None:
        query = select(PortfolioCoin)
        return self._get_all_portfolio_coins(query)

    def create_portfolio_coin(self, portfolio_coin: PortfolioCoin) -> PortfolioCoinSchema | None:
        return self._db_client.create_object(portfolio_coin)

    def patch_portfolio_coin(self, portfolio_coin_id: int,
                             updated_portfolio_coin: dict[str, any]) -> PortfolioCoinSchema | None:
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?
        query = update(PortfolioCoin).where(PortfolioCoin.id == portfolio_coin_id).values(
            portfolio_id=updated_portfolio_coin['portfolio_id'],
            coin_id=updated_portfolio_coin['coin_id'], amount=updated_portfolio_coin['amount'],
            created_at=datetime.now()).returning(PortfolioCoin.portfolio_id, PortfolioCoin.coin_id,
                                                 PortfolioCoin.amount, PortfolioCoin.created_at)
        return self._db_client.update_object(query)

    def delete_portfolio_coin(self, portfolio_coin: PortfolioCoin) -> PortfolioCoinSchema | None:
        return self._db_client.delete_object(portfolio_coin)

    def _get_one_portfolio_coin_by_query(self, query: Select) -> PortfolioCoinSchema | None:
        try:
            return self._db_client.select_one_object_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when portfolio_coin id is not a valid UUID
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_portfolio_coins(self, query: Select) -> PortfolioCoinSchema | None:
        try:
            return self._db_client.select_all_objects(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))
