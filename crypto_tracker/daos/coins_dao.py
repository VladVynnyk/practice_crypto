import logging

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from ..clients.db_client import DBClient
from ..clients.CoinsDBClient import CoinsDBClient
from ..config.database import Coin

logger = logging.getLogger(__name__)


class CoinsDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = CoinsDBClient(uri)

    def get_coin_by_id(self, coin_id: int) -> Coin | None:
        query = select(Coin).where(Coin.id == coin_id)
        return self._get_one_coin_by_query(query)

    def get_all_coins(self) -> Coin | None:
        print("get all coins in dao")
        query = select(Coin)
        return self._get_all_coins(query)

    def patch_coin(self, coin: Coin, updated_fields: dict[str, any]) -> Coin | None:
        for field in updated_fields.keys():
            pass
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?

        coin_id = coin.id
        for field_name, new_value in updated_fields.items():
            setattr(coin, field_name, new_value)

        try:
            return self._db_client.update_coin(coin)
        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

        return self._patch_coin(query)

    def _get_one_coin_by_query(self, query: Select) -> Coin | None:
        try:
            return self._db_client.select_one_coin_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when user id is not a valid UUID
            # if 'invalid UUID' in str(e.sa_exception):
            #     raise InvalidUUIDError(e.description) from e
            logger.error(e.code)
            print(e)
            # raise GetUserError(e.description) from e
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_coins(self, query: Select) -> Coin | None:
        try:
            print("get all coins in _dao")
            return self._db_client.select_all_coins(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))


