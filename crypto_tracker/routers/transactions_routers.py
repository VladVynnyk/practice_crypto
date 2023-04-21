import sys
sys.path.append("..")
from datetime import datetime
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.daos.users_dao import UsersDAO
# from .daos.users_dao import UsersDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import Transaction
from crypto_tracker.api.models.pydantic_models.models import TransactionSchema

Db_uri = get_settings().db_uri

transactions_router = APIRouter(
    prefix="/transactions",
)

#CRUD operations for "transaction" table
@transactions_router.get("/")
def get_transactions():
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        transactions = session.query(Transaction).all()
        return transactions

@transactions_router.get("/{id}")
def get_transaction(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        transaction = session.query(Transaction).where(Transaction.id == id).first()
        return transaction

@transactions_router.post("/")
def add_transaction(transaction: TransactionSchema):
    transaction_for_insert = Transaction(portfolio_id=transaction.portfolio_id, coin_id=transaction.coin_id,
                                         transaction_type=transaction.transaction_type, amount=transaction.amount,
                                         price=transaction.price, created_at=datetime.now())

    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.add(transaction_for_insert)
        session.commit()
    return transaction

@transactions_router.patch("/{id}")
def patch_transaction(id: int, transaction: TransactionSchema):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.query(Transaction).where(Transaction.id == id).update(transaction.dict())
        session.commit()
    return transaction

@transactions_router.delete("/{id}")
def delete_transaction(id: int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        query = session.query(Transaction).where(Transaction.id == id)
        transaction = query.first()
        if not transaction:
            return {"message": "Transaction not found"}
        session.delete(transaction)
        session.commit()
    return {"message": "Transaction deleted"}