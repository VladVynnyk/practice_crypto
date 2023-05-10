
import json
import requests
from typing import List

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


# Function for inserting data into table coin
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


# also to params in this function I can give only coins:List which is sliced only to 20 elements
def insert_coins(coins: List) -> None:
    for coin in coins:
        payload = {
            "fullName": coin["name"],
            "ticker": coin["ticker"]
        }
        request = requests.post("http://127.0.0.1:8000/coins/", json=payload)
        print(request)


# Function, which creates dataclasses from config.json
def convert_config_to_dataclass()->List[ConfigSource]:
    config = read_json_file('config.json')
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