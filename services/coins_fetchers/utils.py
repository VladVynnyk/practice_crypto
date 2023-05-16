
import json
import secrets

import requests
from typing import List, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from starlette import status

from model import ConfigSource, Config


# Function for reading config.json
def read_json_file(filename: str) -> dict:
    with open(filename) as f:
        data = json.load(f)
    return data

# def convert_json_to_dataclass(filename: str):
#     with open(filename) as f:
#         data = json.load(f)
#         sources = [ConfigSource(**s) for s in data['sources']]
#     return sources


# Function for inserting data into table "Coin"
# def insert_coins(coins: List, amount_of_elements: int) -> None:
#     i = 0
#     for coin in coins:
#         if i <= amount_of_elements:
#             coin_for_request = {}
#             payload = {
#                 "fullName": coin["name"],
#                 "ticker": coin["ticker"]
#             }
#             coin_for_request.update({"fullName": coin["name"]})
#             coin_for_request.update({"ticker": coin["symbol"]})
#             print("COIN IN FETCHER: ", coin_for_request)
#             coin_for_request_json = json.dumps(coin_for_request)
#             request = requests.post("http://127.0.0.1:8000/coins/", data=coin_for_request_json)
#             print(request)
#             i += 1
#         else:
#             break


def insert_coins(coins: List) -> None:
    for coin in coins:
        payload = {
            "fullName": coin["name"],
            "ticker": coin["ticker"]
        }
        request = requests.post("http://127.0.0.1:8000/coins/", json=payload)
        print(request)


# Function, which creates dataclasses from config.json
def convert_config_to_dataclass(filename: str)->List[ConfigSource]:
    config = read_json_file(filename)
    list_of_sources = []
    for item in config['sources']:
        print("item", item)
        print("apiKey: ", item['apikey'])
        source = ConfigSource(URL=item['URL'], apikey=item['apikey'],
                              fetcherType=item['fetcherType'])
        list_of_sources.append(source)
    all_config = Config(sources=list_of_sources)
    print("conf sources: ", all_config.sources[0].URL)
    return all_config


def create_requests_to_crypto_api_v2(user_id: int):
    current_user = requests.get(f"http://127.0.0.1:8000/users/{user_id}")
    existing_portfolios = requests.get("http://127.0.0.1:8000/portfolios/user/{id}?user_id="+f"{user_id}")
    # print("PORTFOLIOS: ", existing_portfolios.json())
    if len(existing_portfolios.json()) == 0:
        return {"message": f'{current_user.username}, you must to create portfolio'}
    else:
        coins = []
        for portfolio in existing_portfolios.json():
            # coins_in_portfolio = requests.get(f"http://127.0.0.1:8000/transactions/portfolio/{portfolio.id}")
            coins_in_portfolio = requests.get("http://127.0.0.1:8000/portfolio-coins/portfolio/{id}?portfolio_id="+f"{portfolio['id']}")
            coins.append(coins_in_portfolio.json())
    print("COINS: ", coins)

    return coins


# Function, which creates request to /coins/{id} to fetch ticker or fullName of crypto
def get_tickers_for_coins(coins: dict)->list:
    tickers_for_coins = []
    for coin in coins:
        request_for_ticker_and_fullName = requests.get("http://127.0.0.1:8000/coins/{id}?coin_id="+f"{coin['coin_id']}")
        tickers_for_coins.append(request_for_ticker_and_fullName.json())

    return tickers_for_coins

# Function for calculating PNL
def calculate_pnl_for_portfolio(current_data: list, previous_data: list):
    for item in current_data:
        print(item)
    pass