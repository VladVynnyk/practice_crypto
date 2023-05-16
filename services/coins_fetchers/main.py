import json
import requests
from fetchers import CoinFetcher

from services.coins_fetchers.utils import insert_coins, convert_config_to_dataclass,  \
    create_requests_to_crypto_api_v2, calculate_pnl_for_portfolio, get_tickers_for_coins


# def main():
#     config = read_config()
#     fetchers = get_fetchers(config)
#
#     coins = [fetcher.fetche_coin(config) for fetcher in fetchers]
#
#     post_coins(coins)


def execute_fetchers():
    conf = convert_config_to_dataclass('config.json')

    coins = create_requests_to_crypto_api_v2(1)

    second_fetcher = CoinFetcher(conf, "CoinCap")

    tickers = get_tickers_for_coins(coins[0])

    data = []
    for ticker in tickers:
        print(ticker['fullName'].lower())
        current_data = second_fetcher.fetch_specific_coin(ticker['fullName'].lower())
        data.append(current_data)

    # pnl = calculate_pnl_for_portfolio(current_data=data, previous_data=)



if __name__ == "__main__":
    execute_fetchers()
