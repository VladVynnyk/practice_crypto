import unittest
from unittest.mock import patch, MagicMock, Mock

from fastapi.testclient import TestClient
from fastapi import status
from services.crypto_tracker.main import app

from services.crypto_tracker.src.daos import CoinsDAO
from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.database import Coin
from services.crypto_tracker.src.models import CoinSchema

from services.crypto_tracker.src.settings import get_settings


class TestCoinsDAO:
    client = TestClient(app=app)
    # DB_URI must be mocked
    DB_URI = get_settings().db_uri

    # @patch('services.crypto_tracker.src.daos.coins_dao.DBClient')
    # def test_get_coin_by_id(self):
    #     coins_dao = CoinsDAO(uri=self.DB_URI)
    #     coins = coins_dao.get_coin_by_id(1)
    #     assert coins == {"ticker": "BTC", "id": 1, "fullName": "Bitcoin"}

    # def test_get_coin_by_id(self, mock):
    #     coins_dao = CoinsDAO(uri=self.DB_URI)
    #     coins=coins_dao.get_coin_by_id(1)
    #     assert coins = {"ticker": "BTC", "id": 1, "fullName": "Bitcoin"}

    # @patch('services.crypto_tracker.src.clients.db_client.DBClient')
    def test_get_coin_by_id(self):
        with patch.object(DBClient, 'select_one_object_by_query',
                          return_value={"ticker": "BTC", "fullName": "Bitcoin"}):
            coins_dao = CoinsDAO(uri=self.DB_URI)
            coin = coins_dao.get_coin_by_id(1)
            print("coin: ", coin)
            assert coin == {"ticker": "BTC", "fullName": "Bitcoin"}

    def test_get_all_coins(self, all_coins):
        with patch.object(DBClient, 'select_all_objects', return_value=all_coins):
            coins_dao = CoinsDAO(uri=self.DB_URI)
            coins = coins_dao.get_all_coins()
            assert coins == all_coins

    def test_adding_coin(self):
        with patch.object(DBClient, 'create_object', return_value={"Success": "Object added"}):
            coin = MagicMock(spec=Coin)
            coin.ticker = "TIK"
            coin.fullName = "TikCoin"
            coin_for_insert = {"ticker": coin.ticker, "fullName": coin.fullName}

            coins_dao = CoinsDAO(uri=self.DB_URI)
            result = coins_dao.create_coin(coin_for_insert)
            assert result == {"Success": "Object added"}

    def test_patch_coin(self):
        with patch.object(DBClient, 'update_object', return_value={"id": 2, "ticker": "ETH", "fullName": "Ethereum"}):
            updated_coin = CoinSchema(id=2, ticker="ETH", fullName="Ethereum")
            coin_id = 1
            coins_dao = CoinsDAO(uri=self.DB_URI)
            result = coins_dao.patch_coin(coin_id, updated_coin.dict())
            assert result == updated_coin

    def test_deleting_coin(self):
        # db_client = MagicMock()
        # db_client.get_object_by_query.return_value = {"ticker": "BTC", "id": 1, "fullName": "Bitcoin"}

        with patch.object(DBClient, 'delete_object', return_value={"ticker": "BTC", "fullName": "Bitcoin"}):
            with patch.object(DBClient, 'select_one_object_by_query',
                              return_value={"ticker": "BTC", "fullName": "Bitcoin"}):
                coins_dao = CoinsDAO(uri=self.DB_URI)
                coin_for_delete = coins_dao.get_coin_by_id(1)
                print("Coin for delete: ", coin_for_delete)

                deleted_coin = coins_dao.delete_coin(coin_for_delete)
                assert deleted_coin == {"ticker": "BTC", "fullName": "Bitcoin"}

    def test_deleting_coin_v2(self):
        db_client = DBClient(self.DB_URI)
        db_client.delete_object = MagicMock(return_value={"ticker": "BTC", "fullName": "Bitcoin"})
        db_client.select_one_object_by_query = MagicMock(return_value={"ticker": "BTC", "fullName": "Bitcoin"})

        coins_dao = CoinsDAO(uri=self.DB_URI)
        coins_dao.get_coin_by_id = Mock()
        # coins_dao.get_coin_by_id.return_value = {"ticker": "BTC", "fullName": "Bitcoin"}
        coins_dao.get_coin_by_id.return_value = db_client.select_one_object_by_query()

        # Also here can be logic, where delete_coin returns db_client.delete_object
        coins_dao.delete_coin = Mock()
        # coins_dao.delete_coin.return_value = {"ticker": "BTC", "fullName": "Bitcoin"}
        coins_dao.delete_coin.return_value = db_client.delete_object()

        coin_for_delete = coins_dao.get_coin_by_id(1)
        deleted_coin = coins_dao.delete_coin(coin_for_delete)

        coins_dao.get_coin_by_id.assert_called_once_with(1)
        coins_dao.delete_coin.assert_called_once()

        # check if was called db_client.delete_object method
        db_client.delete_object.assert_called_once()
        # if we will check if method delete_object not called we will get error
        # db_client.delete_object.assert_not_called()
        db_client.select_one_object_by_query.assert_called_once()

        # coins_dao.delete_coin.call_count

        assert deleted_coin == {"ticker": "BTC", "fullName": "Bitcoin"}

    def test_deleting_coin_v3(self):
        db_client = MagicMock()
        delete_object = MagicMock(return_value={"ticker": "BTC", "fullName": "Bitcoin"})
        select_one_object_by_query = MagicMock(return_value={"ticker": "BTC", "fullName": "Bitcoin"})

        db_client.delete_object = delete_object
        db_client.select_one_object_by_query = select_one_object_by_query

        coins_dao = MagicMock()
        get_coin_by_id = MagicMock(return_value=db_client.select_one_object_by_query(1))
        coins_dao.get_coin_by_id = get_coin_by_id

        coin_for_delete = coins_dao.get_coin_by_id(1)
        delete_coin = MagicMock(return_value=db_client.delete_object(coin_for_delete))
        coins_dao.delete_coin = delete_coin

        deleted_coin = coins_dao.delete_coin(coin_for_delete)

        coins_dao.get_coin_by_id.assert_called_once_with(1)
        coins_dao.delete_coin.assert_called_once()

        db_client.delete_object.assert_called_once()
        db_client.select_one_object_by_query.assert_called_once_with(1)

        assert deleted_coin == {"ticker": "BTC", "fullName": "Bitcoin"}
