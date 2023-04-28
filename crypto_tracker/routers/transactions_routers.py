import sys
sys.path.append("..")
from datetime import datetime
from fastapi import APIRouter

from crypto_tracker.daos.transactions_dao import TransactionsDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import Transaction
from crypto_tracker.api.models.pydantic_models.models import TransactionSchema

DB_URI = get_settings().db_uri

transactions_router = APIRouter(
    prefix="/transactions",
)

#CRUD operations for "transaction" table
@transactions_router.get("/")
def get_transactions():
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transactions = transactions_dao.get_all_transactions()
    return transactions


@transactions_router.get("/{id}")
def get_transaction(transaction_id: int):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction = transactions_dao.get_transaction_by_id(transaction_id)
    return transaction


@transactions_router.post("/")
def add_transaction(transaction: TransactionSchema):
    transaction_for_insert = Transaction(portfolio_id=transaction.portfolio_id, coin_id=transaction.coin_id,
                                         transaction_type=transaction.transaction_type, amount=transaction.amount,
                                         price=transaction.price, created_at=datetime.now())
    transaction_dao = TransactionsDAO(uri=DB_URI)
    transaction = transaction_dao.create_transaction(transaction_for_insert)
    return transaction


@transactions_router.patch("/{id}")
def patch_transaction(transaction_id: int, updated_transaction: TransactionSchema):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction_to_update = transactions_dao.patch_transaction(transaction_id, updated_transaction.dict())
    return transaction_to_update


@transactions_router.delete("/{id}")
def delete_transaction(transaction_id: int):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction_for_delete = transactions_dao.get_transaction_by_id(transaction_id)
    obj_to_delete = transactions_dao.delete_transaction(transaction_for_delete)
    return obj_to_delete

