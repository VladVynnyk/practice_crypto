from abc import ABC, abstractmethod
from typing import List

import requests

from services.coins_fetchers.model import CoinDetails

from utils import read_json_file, convert_config_to_dataclass


# class CoinFetcher(ABC):
class Fetcher(ABC):

    @abstractmethod
    def fetch_all_coins(self) -> CoinDetails:
        raise NotImplementedError("This method needs to be implemented")


class CoinFetcher(Fetcher):
    def __init__(self, filename: str) -> None:
        self.config = convert_config_to_dataclass()

    def fetch_all_coins(self, amount_of_coins) -> List[CoinDetails]:
        print("CONFIG: ", self.config)
        url = self.config.sources[0].URL
        # it's for limit amount of coins
        limited_url = url + f'?limit={amount_of_coins}'
        print("Limited url " + limited_url)
        headers = {"X-CMC_PRO_API_KEY": self.config.sources[0].apikey}
        request = requests.get(limited_url, headers=headers)
        return request.json()