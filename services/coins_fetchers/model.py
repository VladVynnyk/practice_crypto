from dataclasses import dataclass

from decimal import Decimal


@dataclass
class CoinDetails:
    name: str
    rate: Decimal


@dataclass
class FetcherConfig:
    name: str
    rate: Decimal
