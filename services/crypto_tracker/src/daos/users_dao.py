from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import OperationalError

from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.database import User
from services.crypto_tracker.src.models import UserSchema

logger = logging.getLogger(__name__)


class UsersDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        self._db_client = DBClient(uri)

    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        query = select(User).where(User.id == user_id)
        return self._get_one_user_by_query(query)

    def get_user_by_username(self, username: str) -> UserSchema | None:
        query = select(User).where(User.username == username)
        return self._get_one_user_by_query(query)

    def get_user_for_operation(self, user_id: int)-> UserSchema | None:
        query = select(User).where(User.id == user_id)
        return self._db_client.select_one_object_for_operation(query)

    def get_all_users(self) -> UserSchema | None:
        query = select(User)
        return self._get_all_users(query)

    def create_user(self, user: User) -> UserSchema | None:
        return self._db_client.create_object(user)

    def patch_user(self, user_id: int, updated_user: dict[str, any]) -> UserSchema | None:
        # todo: check for unique fields ?
        # todo: is it a bug: DB records does not get updated when the same info passed several times?
        query = update(User).where(User.id == user_id).values(username=updated_user['username'], email=updated_user['email'], password=updated_user['password'], created_at=datetime.now()).returning(User.id, User.username, User.email, User.password, User.created_at)
        return self._db_client.update_object(query)

    def delete_user(self, user: User) -> UserSchema | None:
        return self._db_client.delete_object(user)

    def _get_one_user_by_query(self, query: Select) -> UserSchema | None:
        try:
            return self._db_client.select_one_object_by_query(query)

        except OperationalError as e:
            # NOTE: case for the "DBAPIError" when user id is not a valid UUID
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

    def _get_all_users(self, query: Select) -> UserSchema | None:
        try:
            return self._db_client.select_all_objects(query)

        except OperationalError as e:
            logger.error(e.code)
            print(e)
            raise OperationalError("Operational error: ", str(e), str(e.orig))

