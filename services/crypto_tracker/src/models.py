from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str

class UserSchemaRegister(BaseModel):
    username: str
    email: str
    password: str
    confirmed_password: str

class PortfolioSchema(BaseModel):
    user_id: int
    name: str


class CoinSchema(BaseModel):
    id: int
    ticker: str
    fullName: str


class PortfolioCoinSchema(BaseModel):
    portfolio_id: int
    coin_id: int
    amount: float


class TransactionSchema(BaseModel):
    portfolio_id: int
    coin_id: int
    transaction_type: str
    amount: float
    price: float

