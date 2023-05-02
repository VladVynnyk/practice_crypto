from fastapi.testclient import TestClient
from fastapi import status
from services.crypto_tracker.main import app


class TestCoinsEndpoints:
    client = TestClient(app=app)

    def test_hello_endpoint(self):
        response = self.client.get('/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello World"}

    def test_get_all_coins(self):
        response = self.client.get('/coins')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
    {
    "ticker": "BTC",
    "id": 1,
    "fullName": "Bitcoin"
    },
    {
    "ticker": "ETH",
    "id": 2,
    "fullName": "Ethereum"
    },
    {
    "ticker": "DOT",
    "id": 4,
    "fullName": "Polkadot"
    },
    {
    "ticker": "ATOM",
    "id": 7,
    "fullName": "Cosmos"
    },
    {
    "ticker": "LINK",
    "id": 13,
    "fullName": "ChainLink"
    },
    {
    "ticker": "stri",
    "id": 17,
    "fullName": "stri"
    },
    {
    "ticker": "SOME NEW COIN Now",
    "id": 23,
    "fullName": "SNN"
    },
    {
    "ticker": "NEW",
    "id": 26,
    "fullName": "NEW"
    },
    {
    "ticker": "SOT",
    "id": 29,
    "fullName": "SOMETHING"
    },
    {
    "ticker": "USDT",
    "id": 25,
    "fullName": "Tether"
    },
    {
    "ticker": "UNI",
    "id": 30,
    "fullName": "UniSwap"
    },
    {
    "ticker": "MANA",
    "id": 27,
    "fullName": "Decentraland"
    },
    {
    "ticker": "LTC",
    "id": 33,
    "fullName": "Litecoin"
    },
    {
    "ticker": "NMC",
    "id": 34,
    "fullName": "Namecoin"
    },
    {
    "ticker": "TRC",
    "id": 35,
    "fullName": "Terracoin"
    },
    {
    "ticker": "PPC",
    "id": 36,
    "fullName": "Peercoin"
    },
    {
    "ticker": "NVC",
    "id": 37,
    "fullName": "Novacoin"
    },
    {
    "ticker": "FTC",
    "id": 38,
    "fullName": "Feathercoin"
    },
    {
    "ticker": "FRC",
    "id": 39,
    "fullName": "Freicoin"
    },
    {
    "ticker": "IXC",
    "id": 40,
    "fullName": "Ixcoin"
    },
    {
    "ticker": "WDC",
    "id": 41,
    "fullName": "WorldCoin"
    },
    {
    "ticker": "DGC",
    "id": 42,
    "fullName": "Digitalcoin"
    },
    {
    "ticker": "GLC",
    "id": 43,
    "fullName": "Goldcoin"
    },
    {
    "ticker": "PXC",
    "id": 44,
    "fullName": "Phoenixcoin"
    },
    {
    "ticker": "XPM",
    "id": 45,
    "fullName": "Primecoin"
    },
    {
    "ticker": "ANC",
    "id": 46,
    "fullName": "Anoncoin"
    },
    {
    "ticker": "CSC",
    "id": 47,
    "fullName": "CasinoCoin"
    },
    {
    "ticker": "XRP",
    "id": 48,
    "fullName": "XRP"
    },
    {
    "ticker": "QRK",
    "id": 49,
    "fullName": "Quark"
    },
    {
    "ticker": "ZET",
    "id": 50,
    "fullName": "Zetacoin"
    },
    {
    "ticker": "TAG",
    "id": 51,
    "fullName": "TagCoin"
    },
    {
    "ticker": "PIN",
    "id": 52,
    "fullName": "Public Index Network"
    }
    ]

    def test_get_one_coin(self):
        response = self.client.get('/coins/{id}?coin_id=1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"ticker": "BTC", "id": 1, "fullName": "Bitcoin"}

    # def test_insert_coin(self):
    #     response = self.client.post('/coins', content={"ticker": "ETC", "fullName": "Ethereum classic"})
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == {"ticker": "ETC", "fullName": "Ethereum classic"}