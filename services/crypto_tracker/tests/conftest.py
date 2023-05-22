from typing import List

import pytest


@pytest.fixture(scope="session")
def all_coins()->List:
    return [
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
  },
  {
    "ticker": "string",
    "id": 53,
    "fullName": "string"
  }
]


@pytest.fixture(scope="session")
def all_transactions()->List:
    return [
      [
        {
          "transaction_type": "BUY",
          "id": 1,
          "price": 20000,
          "portfolio_id": 1,
          "coin_id": 1,
          "amount": 1,
          "created_at": "2023-05-20T08:21:28.918310"
        },
        {
          "transaction_type": "buy",
          "id": 2,
          "price": 20000,
          "portfolio_id": 1,
          "coin_id": 1,
          "amount": 1,
          "created_at": "2023-05-20T08:31:01.805462"
        },
        {
          "transaction_type": "buy",
          "id": 3,
          "price": 20000,
          "portfolio_id": 1,
          "coin_id": 1,
          "amount": 1,
          "created_at": "2023-05-20T08:34:48.924140"
        }
      ]
]