import sys

from services.crypto_tracker.src.middleware import auth
from services.crypto_tracker.src.routers.portfolio_coins_routers import add_portfolio_coin

# sys.path.append("../..")
import requests
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from services.crypto_tracker.src.daos.transactions_dao import TransactionsDAO
from services.crypto_tracker.src.settings import get_settings

# It's will be temporary imports
from services.crypto_tracker.src.database import Transaction
from services.crypto_tracker.src.models import TransactionSchema

DB_URI = get_settings().db_uri

transactions_router = APIRouter(
    prefix="/transactions",
)


# CRUD operations for "transaction" table
@transactions_router.get("/")
def get_transactions(api_key: APIKey = Depends(auth.get_api_key)):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transactions = transactions_dao.get_all_transactions()
    return transactions


@transactions_router.get("/{id}")
def get_transaction_by_id(transaction_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction = transactions_dao.get_transaction_by_id(transaction_id)

    response = {"portfolio_id": transaction[0].portfolio_id, "coin_id": transaction[0].coin_id,
                "transaction_type": transaction[0].transaction_type, "amount": transaction[0].amount,
                "price": transaction[0].price, "created_at": transaction[0].created_at}
    return response


@transactions_router.get("/portfolio/{id}")
def get_transactions_by_portfolio_id(portfolio_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transactions = transactions_dao.get_transactions_by_portfolio_id(portfolio_id)
    return transactions


@transactions_router.post("/")
def add_transaction(transaction: TransactionSchema, api_key: APIKey = Depends(auth.get_api_key)):
    transaction_for_insert = Transaction(portfolio_id=transaction.portfolio_id, coin_id=transaction.coin_id,
                                         transaction_type=transaction.transaction_type, amount=transaction.amount,
                                         price=transaction.price, created_at=datetime.now())
    transaction_dao = TransactionsDAO(uri=DB_URI)
    inserted_transaction = transaction_dao.create_transaction(transaction_for_insert)

    if transaction.transaction_type.lower() == "buy":
        body_for_request_to_portfolio_coins = {
            'portfolio_id': transaction.portfolio_id,
            'coin_id': transaction.coin_id,
            'amount': transaction.amount
        }

        # response = requests.post("http://127.0.0.1:8000/portfolio-coins/", json=body_for_request_to_portfolio_coins)
        # print(request.json())
    response = add_portfolio_coin(body_for_request_to_portfolio_coins)
    print("Response: ", response)
    # elif transaction.transaction_type == "SELL" or "Sell" or "sell":
        # Logic for transaction
        # request_for_initial_price = requests.get(f"http://127.0.0.1:8000/portfolio-coins/{}")
        # body_for_request_to_patch_portfolio_coins = {
        #     'portfolio_id': transaction.portfolio_id,
        #     'coin_id': transaction.coin_id,
        #     'amount': transaction.amount
        # }
        # request = requests.patch(f"http://127.0.0.1:8000/portfolio-coins/{transaction.coin_id}", json=)
    return inserted_transaction


@transactions_router.patch("/{id}")
def patch_transaction(transaction_id: int, updated_transaction: TransactionSchema, api_key: APIKey = Depends(auth.get_api_key)):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction_to_update = transactions_dao.patch_transaction(transaction_id, updated_transaction.dict())
    return transaction_to_update


@transactions_router.delete("/{id}")
def delete_transaction(transaction_id: int, api_key: APIKey = Depends(auth.get_api_key)):
    transactions_dao = TransactionsDAO(uri=DB_URI)
    transaction_for_delete = transactions_dao.get_transaction_by_id(transaction_id)
    obj_to_delete = transactions_dao.delete_transaction(transaction_for_delete)
    return obj_to_delete
