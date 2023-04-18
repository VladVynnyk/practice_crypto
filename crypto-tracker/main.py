from typing import Union

from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from api.models.pydantic_models.models import UserModel, CoinModel, PortfolioModel, PortfolioCoinModel, TransactionModel
from config.database import User, Coin, Portfolio, PortfolioCoin, Transaction


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#CRUD for "coin" table
@app.post("/coin")
def add_coin(coin: CoinModel):
    coin_for_insert = Coin(ticker=coin.ticker, fullName=coin.fullName)

    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.add(coin_for_insert)
        session.commit()
    return coin


@app.get("/coins")
def get_coins():
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        coins = session.query(Coin).all()
        return coins

@app.get("/coin/{id}")
def get_coin(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        coin = session.query(Coin).where(Coin.id == id).first()
        return coin

@app.patch("/coin/{id}")
def update_coin(id, coin: CoinModel):
    # coin_for_update = Coin(ticker=coin.ticker, fullName=coin.fullName)

    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.query(Coin).where(Coin.id == id).update(coin.dict())
        session.commit()
    return coin

@app.delete("/coin/{id}")
def delete_coin(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        query = session.query(Coin).where(Coin.id == id)
        coin = query.first()
        if not coin:
            return {"message": "Coin not found"}
        session.delete(coin)
        session.commit()
    return {"message": "Coin deleted"}

#CRUD for "user" table
@app.get("/users")
def get_users():
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        users = session.query(User).all()
        return users

@app.get("/user/{id}")
def get_user(id):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        user = session.query(User).where(User.id==id).first()
        return user


@app.post("/user")
def add_user(user: UserModel):

    user_for_insert = User(username=user.username, email=user.email, password=user.password, created_at=datetime.now())

    Session= scoped_session(sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.add(user_for_insert)
        session.commit()
    return user


#but for deleting and updating user must be param id in this functions
@app.delete("/user/{id}")
def delete_user(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        query = session.query(User).where(User.id == id)
        user = query.first()
        if not user:
            return {"message": "User not found"}
        session.delete(user)
        session.commit()
    return {"message": "User deleted"}

@app.patch("/user/{id}")
def patch_user(id: int, user: UserModel):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.query(User).where(User.id == id).update(user.dict())
        session.commit()
    return user


#CRUD for "portfolio" table
@app.get("/portfolios")
def get_portfolios():
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        portfolios = session.query(Portfolio).all()
        return portfolios

@app.get("/portfolio/{id}")
def get_portfolio(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        portfolio = session.query(Portfolio).where(Portfolio.id == id).first()
        return portfolio

@app.post("/portfolio")
def add_portfolio(portfolio: PortfolioModel):
    portfolio_for_insert = Portfolio(user_id=portfolio.user_id, name=portfolio.name, created_at=datetime.now())

    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.add(portfolio_for_insert)
        session.commit()
    return portfolio

@app.patch("/portfolio/{id}")
def patch_portfolio(id: int, portfolio: PortfolioModel):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.query(Portfolio).where(Portfolio.id == id).update(portfolio.dict())
        session.commit()
    return portfolio

@app.delete("/portfolio/{id}")
def delete_portfolio(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        query = session.query(Portfolio).where(Portfolio.id == id)
        portfolio = query.first()
        if not portfolio:
            return {"message": "Portfolio not found"}
        session.delete(portfolio)
        session.commit()
    return {"message": "Portfolio deleted"}

#CRUD operations for "transaction" table
@app.get("/transactions")
def get_transactions():
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        transactions = session.query(Transaction).all()
        return transactions

@app.get("/transaction/{id}")
def get_transaction(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        transaction = session.query(Transaction).where(Transaction.id == id).first()
        return transaction

@app.post("/transaction")
def add_transaction(transaction: TransactionModel):
    transaction_for_insert = Transaction(portfolio_id=transaction.portfolio_id, coin_id=transaction.coin_id,
                                         transaction_type=transaction.transaction_type, amount=transaction.amount,
                                         price=transaction.price, created_at=datetime.now())

    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.add(transaction_for_insert)
        session.commit()
    return transaction

@app.patch("/transaction/{id}")
def patch_transaction(id: int, transaction: TransactionModel):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.query(Transaction).where(Transaction.id == id).update(transaction.dict())
        session.commit()
    return transaction

@app.delete("/transaction/{id}")
def delete_transaction(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        query = session.query(Transaction).where(Transaction.id == id)
        transaction = query.first()
        if not transaction:
            return {"message": "Transaction not found"}
        session.delete(transaction)
        session.commit()
    return {"message": "Transaction deleted"}


#CRUD operations for "PortfolioCoin" table
@app.get("/portfolioCoin")
def get_portfolioCoins():
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        portfolioCoins = session.query(PortfolioCoin).all()
        return portfolioCoins

@app.get("/portfolioCoin/{id}")
def get_portfolioCoin(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        portfolioCoin = session.query(PortfolioCoin).where(PortfolioCoin.id == id).first()
        return portfolioCoin

@app.post("/portfolioCoin")
def add_portfolioCoin(portfolioCoin: PortfolioCoinModel):
    portfolioCoin_for_insert = PortfolioCoin(portfolio_id=portfolioCoin.portfolio_id, coin_id=portfolioCoin.coin_id,
                                             amount=portfolioCoin.amount, created_at=portfolioCoin.created_at)

    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.add(portfolioCoin_for_insert)
        session.commit()
    return portfolioCoin

@app.patch("/portfolioCoin/{id}")
def patch_portfolioCoin(id: int, portfolioCoin: PortfolioCoinModel):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        session.query(PortfolioCoin).where(PortfolioCoin.id == id).update(portfolioCoin.dict())
        session.commit()
    return portfolioCoin

@app.delete("/portfolioCoin/{id}")
def delete_portfolioCoin(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb')))
    with Session() as session:
        query = session.query(PortfolioCoin).where(PortfolioCoin.id==id)
        portfolio_coin = query.first()
        if not portfolio_coin:
            return {"message": "PortfolioCoin not found"}
        session.delete(portfolio_coin)
        session.commit()
    return {"message": "PortfolioCoin deleted"}