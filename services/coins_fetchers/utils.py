
import json
import secrets

import requests
from typing import List, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from starlette import status

from services.coins_fetchers.model import ConfigSource, Config


import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

# Function for reading config.json
def read_json_file(filename: str) -> dict:
    with open(filename) as f:
        data = json.load(f)
    return data


headers={"access_token": "my_key"}
def insert_coins(coins: List, local_api_url: str) -> None:
    for coin in coins:
        payload = {
            "fullName": coin["name"],
            "ticker": coin["ticker"]
        }
        request = requests.post(f"{local_api_url}/coins/", json=payload, headers=headers)
        print(request)


# Function, which creates dataclasses from config.json
def convert_config_to_dataclass(filename: str)->List[ConfigSource]:
    config = read_json_file(filename)
    list_of_sources = []
    for item in config['sources']:
        # print("Item: ", config['sources'][item])
        source = ConfigSource(url=config['sources'][item][0], apikey=config['sources'][item][1], fetcherType="")
        list_of_sources.append(source)
    all_config = Config(sources=list_of_sources)
    return all_config


def create_requests_to_crypto_api_v2(user_id: int, local_api_url: str)->list:
    current_user = requests.get(f"{local_api_url}/users/"+"{id}"+"?user_id="+f"{user_id}", headers=headers)
    print("cur user: ", current_user.json())
    existing_portfolios = requests.get(f"{local_api_url}/portfolios/user/"+"{id}"+"?user_id="+f"{user_id}", headers=headers)
    print("PORTFOLIOS: ", existing_portfolios.json())
    if len(existing_portfolios.json()) == 0:
        return {"message": 'You must to create portfolio'}
    else:
        coins = []
        for portfolio in existing_portfolios.json():
            coins_in_portfolio = requests.get(f"{local_api_url}/portfolio-coins/portfolio/"+"{id}"+"?portfolio_id="+f"{portfolio['id']}", headers=headers)
            coins.append(coins_in_portfolio.json())
    print("COINS: ", coins)

    return coins


# Function, which creates request to /coins/{id} to fetch ticker or fullName of crypto
def get_tickers_for_coins(coins: dict, local_api_url: str)->list:
    tickers_for_coins = []
    for coin in coins:
        request_for_ticker_and_fullName = requests.get(f"{local_api_url}/coins/"+"{id}"+f"?coin_id="+f"{coin['coin_id']}", headers=headers)
        tickers_for_coins.append(request_for_ticker_and_fullName.json())

    return tickers_for_coins

# Function for calculating PNL
def calculate_pnl_for_portfolio(current_data: list, previous_data: list):
    for item in current_data:
        print(item)
    pass