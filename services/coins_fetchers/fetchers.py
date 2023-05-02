from abc import ABC, abstractmethod
import requests

from services.coins_fetchers.model import CoinDetails

from utils import read_json_file


# class CoinFetcher(ABC):
class Fetcher(ABC):
    # @abstractmethod
    # def fetch_coin(self, config: ) -> CoinDetails:
    #     raise NotImplementedError()

    @abstractmethod
    def fetch_coin(self, config: dict) -> CoinDetails:
        # raise NotImplementedError()
        pass

    @abstractmethod
    def fetch_all_coins(self, config: dict) -> CoinDetails:
        # raise NotImplementedError()
        pass

class CoinFetcher(Fetcher):
    def __init__(self, filename: str) -> None:
        self.config = read_json_file(filename)

    def fetch_coin(self, config: dict) -> CoinDetails:
        pass

    def fetch_all_coins(self) -> CoinDetails:
        print("CONFIG: ", self.config)
        url = self.config['sources'][0]['URL']
        headers = {"X-CMC_PRO_API_KEY": self.config['sources'][0]['apikey']}
        request = requests.get(url, headers=headers)
        return request.json()
