import json
import requests
from typing import List


# Function for reading config.json
def read_json_file(filename: str) -> dict:
    with open(filename) as f:
        data = json.load(f)
    return data

# Function for inserting data into table coin
def insert_coins(coins: List, amount_of_elements: int):
    i = 0
    for coin in coins:
        if i <= amount_of_elements:
            coin_for_request = {}
            coin_for_request.update({"fullName": coin["name"]})
            coin_for_request.update({"ticker": coin["symbol"]})
            print("COIN IN FETCHER: ", coin_for_request)
            coin_for_request_json = json.dumps(coin_for_request)
            request = requests.post("http://127.0.0.1:8000/coins/", data=coin_for_request_json)
            print(request)
            i += 1
        else:
            break