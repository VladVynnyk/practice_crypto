import logging

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from ..clients.db_client import DBClient
from ..config.database import Coin

logger = logging.getLogger(__name__)


class CoinsDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = DBClient(uri)

    def get_coin_by_id(self, coin_id: int) -> Coin | None:
        query = select(Coin).where(Coin.id == coin_id)
        return self._get_one_coin_by_query(query)

    def get_coin_for_operation(self, coin_id: int)-> Coin | None:
        query = select(Coin).where(Coin.id == coin_id)
        return self._db_client.select_one_object_for_operation(query)

    def get_all_coins(self) -> Coin | None:
        query = select(Coin)
        return self._get_all_coins(query)

    def create_coin(self, coin: Coin):
        return self._db_client.create_object(coin)

    def patch_coin(self, coin_id: int, updated_coin: dict[str, any]) -> Coin | None:
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?
        query = update(Coin).where(Coin.id == coin_id).values(ticker=updated_coin['ticker'], fullName=updated_coin['fullName'])
        return self._db_client.update_object(query)

    def delete_coin(self, coin: Coin) -> Coin | None:
        return self._db_client.delete_object(coin)

    def _get_one_coin_by_query(self, query: Select) -> Coin | None:
        try:
            return self._db_client.select_one_object_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when user id is not a valid UUID
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_coins(self, query: Select) -> Coin | None:
        try:
            return self._db_client.select_all_objects(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))
