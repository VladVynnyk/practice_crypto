from unittest.mock import patch, MagicMock, Mock

import pytest
from sqlalchemy import Select
from sqlalchemy.exc import OperationalError

from services.crypto_tracker.main import app
from fastapi.testclient import TestClient

from services.crypto_tracker.src.models import TransactionSchema
from services.crypto_tracker.src.settings import get_settings

from services.crypto_tracker.src.clients.db_client import DBClient

from services.crypto_tracker.src.daos.transactions_dao import TransactionsDAO


class TestTransactionsDAO:
    client = TestClient(app=app)
    DB_URI = get_settings().db_uri

    def test_transaction_by_id(self):
        with patch.object(DBClient, 'select_one_object_by_query',
                          return_value={
                                "id": 3,
                                "coin_id": 2,
                                "amount": 1,
                                "created_at": "2023-04-20T15:59:22.225058",
                                "transaction_type": "Buy",
                                "portfolio_id": 2,
                                "price": 1000
                              }):
            transactions_dao = TransactionsDAO(uri=self.DB_URI)
            transaction = transactions_dao.get_transaction_by_id(3)
            print("coin: ", transaction)
            assert transaction == {
                                "id": 3,
                                "coin_id": 2,
                                "amount": 1,
                                "created_at": "2023-04-20T15:59:22.225058",
                                "transaction_type": "Buy",
                                "portfolio_id": 2,
                                "price": 1000
                              }

    def test_get_all_transactions(self, all_transactions):
        with patch.object(DBClient, 'select_all_objects', return_value=all_transactions):
            transactions_dao = TransactionsDAO(uri=self.DB_URI)
            transactions = transactions_dao.get_all_transactions()
        assert transactions == all_transactions
