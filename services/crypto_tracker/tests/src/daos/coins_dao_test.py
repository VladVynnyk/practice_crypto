from fastapi.testclient import TestClient
from fastapi import status
from services.crypto_tracker.main import app
from services.crypto_tracker.src.daos import CoinsDAO

from services.crypto_tracker.src.settings import get_settings


class TestCoinsDAO:
    client = TestClient(app=app)
    DB_URI = get_settings().db_uri

    def test_get_one_coin(self):
        coins_dao = CoinsDAO(uri=self.DB_URI)
        coins = coins_dao.get_coin_by_id(1)
        assert coins == {"ticker": "BTC", "id": 1, "fullName": "Bitcoin"}
