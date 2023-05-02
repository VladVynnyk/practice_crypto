import json
import requests
from fetchers import CoinFetcher

from services.coins_fetchers.utils import insert_coins

# def main():
#     config = read_config()
#     fetchers = get_fetchers(config)
#
#     coins = [fetcher.fetche_coin(config) for fetcher in fetchers]
#
#     post_coins(coins)


def main():
    coin_fetcher = CoinFetcher('config.json')
    coins = coin_fetcher.fetch_all_coins()

    print("COINS: ", coins['data'])

    insert_coins(coins['data'], 20)

main()