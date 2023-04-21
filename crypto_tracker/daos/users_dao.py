from __future__ import annotations

import logging
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError

from ..clients.db_client import DBClient
from crypto_tracker.config.database import User

from sqlalchemy import select

logger = logging.getLogger(__name__)


class UsersDAO:
    _instance: UsersDAO = None

    def __new__(cls, *args, **kwargs) -> UsersDAO:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._db_client = DBClient()

    def get_all_users(self, filters=None) -> list:
        query = ''
        return self._execute(query)

    def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        return self._get_user_by_query(query)

    def _execute(self, query) -> any:
        try:
            return self._db_client.execute_query_one(query)
        except DatabaseError as e:
            logger.error(f'{e}')
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"{e}")
        except Exception as e:
            logger.error(f'{e}')
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"{e}")
