from dataclasses import dataclass

from decimal import Decimal
from typing import List


@dataclass
class CoinDetails:
    name: str
    rate: Decimal


@dataclass
class FetcherConfig:
    name: str
    rate: Decimal

@dataclass
class ConfigSource:
    URL: str
    apikey: str
    fetcherType: str

@dataclass
class Config:
    sources: List[ConfigSource]