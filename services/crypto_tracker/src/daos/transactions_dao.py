from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.database import Transaction
from services.crypto_tracker.src.models import TransactionSchema

logger = logging.getLogger(__name__)


class TransactionsDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = DBClient(uri)

    def get_transaction_by_id(self, transaction_id: int) -> TransactionSchema | None:
        query = select(Transaction).where(Transaction.id == transaction_id)
        return self._get_one_transaction_by_query(query)

    def get_transaction_for_operation(self, transaction_id: int) -> TransactionSchema | None:
        query = select(Transaction).where(Transaction.id == transaction_id)
        return self._db_client.select_one_object_for_operation(query)

    def get_all_transactions(self) -> TransactionSchema | None:
        query = select(Transaction)
        return self._get_all_transactions(query)

    def create_transaction(self, transaction: Transaction) -> TransactionSchema | None:
        return self._db_client.create_object(transaction)

    def patch_transaction(self, transaction_id: int, updated_transaction: dict[str, any]) -> TransactionSchema | None:
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?
        query = update(Transaction).where(Transaction.id == transaction_id).values(
            portfolio_id=updated_transaction['portfolio_id'],
            coin_id=updated_transaction['coin_id'], transaction_type=updated_transaction['transaction_type'],
            amount=updated_transaction['amount'], price=updated_transaction['price'],
            created_at=datetime.now()).returning(Transaction.id, Transaction.portfolio_id, Transaction.coin_id,
                                                 Transaction.transaction_type, Transaction.amount, Transaction.price,
                                                 Transaction.created_at)
        return self._db_client.update_object(query)

    def delete_transaction(self, transaction: Transaction) -> TransactionSchema | None:
        return self._db_client.delete_object(transaction)

    def _get_one_transaction_by_query(self, query: Select) -> TransactionSchema | None:
        try:
            return self._db_client.select_one_object_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when transaction id is not a valid UUID
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_transactions(self, query: Select) -> TransactionSchema | None:
        try:
            return self._db_client.select_all_objects(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))
