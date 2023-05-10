import json

from fastapi.testclient import TestClient
from fastapi import status

from services.crypto_tracker.main import app
from services.crypto_tracker.tests.conftest import all_coins

class TestCoinsEndpoints:
    client = TestClient(app=app)

    # def test_hello_endpoint(self):
    #     response = self.client.get('/')
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == {"message": "Hello World"}
    #
    # def test_get_all_coins(self, all_coins):
    #     response = self.client.get('/coins')
    #     expected_data = json.dumps(all_coins)
    #     print(expected_data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == expected_data
    #
    # def test_get_one_coin(self):
    #     response = self.client.get('/coins/{id}?coin_id=1')
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == {"ticker": "BTC", "fullName": "Bitcoin"}

    # def test_insert_coin(self):
    #     response = self.client.post('/coins', content={"ticker": "ETC", "fullName": "Ethereum classic"})
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == {"ticker": "ETC", "fullName": "Ethereum classic"}