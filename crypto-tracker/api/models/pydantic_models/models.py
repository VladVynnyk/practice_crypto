from datetime import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    # id: int
    username: str
    email: str
    password: str
    created_at: datetime


class PortfolioModel(BaseModel):
    #id: int
    user_id: int
    name: str
    created_at: datetime
    # portfolioCoin:
    # transaction:


class CoinModel(BaseModel):
    #id: int
    ticker: str
    fullName: str
    # transaction:


class PortfolioCoinModel(BaseModel):
    #id: int
    portfolio_id: int
    coin_id: int
    amount: float
    created_at: datetime


class TransactionModel(BaseModel):
    #id: int
    portfolio_id: int
    coin_id: int
    transaction_type: str
    amount: float
    price: float
    created_at: datetime