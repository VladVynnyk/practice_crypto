from abc import ABC, abstractmethod
from typing import List, Literal

import requests

from services.coins_fetchers.model import CoinDetails, CoinPrice

from services.coins_fetchers.utils import read_json_file, convert_config_to_dataclass


# class CoinFetcher(ABC):
class Fetcher(ABC):

    @abstractmethod
    def fetch_all_coins(self) -> CoinDetails:
        raise NotImplementedError("This method needs to be implemented")


class CoinFetcher(Fetcher):
    def __init__(self, config, source: str) -> None:
        self.config = config
        self.source = source

    def fetch_all_coins(self, amount_of_coins) -> List[CoinDetails]:
        print("CONFIG: ", self.config)
        # url = self.config.sources[0].URL
        url = self.config.sources["CoinCap"][0]
        # it's for limit amount of coins
        limited_url = url + f'?limit={amount_of_coins}'
        print("Limited url " + limited_url)
        headers = {"X-CMC_PRO_API_KEY": self.config.sources[0].apikey}
        request = requests.get(limited_url, headers=headers)
        return request.json()

    def fetch_specific_coin(self, coin: str) -> CoinPrice:
        if self.source.lower() == "coinmarketcap":
            # url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=BTC,ETC"

            # coin here must be like a ticker. Example: BTC, ETH
            url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol={coin["ticker"]}'
            headers = {"X-CMC_PRO_API_KEY": self.config.sources[0].apikey}
            request = requests.get(url, headers=headers)
            return request.json()

        elif self.source.lower() == "coincap":
            # coin here must be like a slug. Example: bitcoin, ethereum
            # url = f'https://api.coincap.io/v2/assets/{coin}'
            print("SELF.CONFING", self.config)
            url = self.config.sources[1].url
            print("URL: ", url)

            request = requests.get(f"{url}"+"/"+f"{coin['fullName'].lower()}")
            print(request.json())
            return request.json()

        else:
            return {"message": "Source not found"}
