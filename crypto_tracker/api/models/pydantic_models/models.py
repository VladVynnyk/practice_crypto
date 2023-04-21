from datetime import datetime
from pydantic import BaseModel

class UserSchema(BaseModel):
    # id: int
    username: str
    email: str
    password: str
    created_at: datetime


class PortfolioSchema(BaseModel):
    #id: int
    user_id: int
    name: str
    created_at: datetime
    # portfolioCoin:
    # transaction:


class CoinSchema(BaseModel):
    #id: int
    ticker: str
    fullName: str
    # transaction:


class PortfolioCoinSchema(BaseModel):
    #id: int
    portfolio_id: int
    coin_id: int
    amount: float
    created_at: datetime


class TransactionSchema(BaseModel):
    #id: int
    portfolio_id: int
    coin_id: int
    transaction_type: str
    amount: float
    price: float
    created_at: datetime