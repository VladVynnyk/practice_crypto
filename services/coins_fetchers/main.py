import json
import requests
import sys
sys.path.append("../..")

from services.crypto_tracker.src.settings import get_settings

from services.coins_fetchers.fetchers import CoinFetcher

from services.coins_fetchers.utils import insert_coins, convert_config_to_dataclass,  \
    create_requests_to_crypto_api_v2, calculate_pnl_for_portfolio, get_tickers_for_coins


url_to_local_api_in_docker = get_settings().url_to_local_api



# def main():
#     config = read_config()
#     fetchers = get_fetchers(config)
#
#     coins = [fetcher.fetche_coin(config) for fetcher in fetchers]
#
#     post_coins(coins)


def execute_fetchers(user_id: int, source: str):
    conf = convert_config_to_dataclass('../coins_fetchers/config.json')
    coins_of_user = create_requests_to_crypto_api_v2(user_id, url_to_local_api_in_docker)

    second_fetcher = CoinFetcher(conf, source)

    tickers = get_tickers_for_coins(coins_of_user[0], url_to_local_api_in_docker)
    print("tickers: ", tickers)
    data = []
    for ticker in tickers:
        print(ticker['fullName'].lower())
        current_data = second_fetcher.fetch_specific_coin(ticker)
        data.append(current_data)

    # pnl = calculate_pnl_for_portfolio(current_data=data, previous_data=)
    return data


if __name__ == "__main__":
    execute_fetchers()
