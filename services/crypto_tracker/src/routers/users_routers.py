import sys
sys.path.append("../../..")
from fastapi import APIRouter
from datetime import datetime

from services.crypto_tracker.src.daos.users_dao import UsersDAO
from services.crypto_tracker.src.settings import get_settings

# It's will be temporary imports
from services.crypto_tracker.src.database import User
from services.crypto_tracker.src.models import UserSchema

DB_URI = get_settings().db_uri

users_router = APIRouter(
    prefix="/users",
)

# CRUD for "user" table
@users_router.get("/")
def get_users():
    users_dao = UsersDAO(uri=DB_URI)
    users = users_dao.get_all_users()
    return users

@users_router.get("/{id}")
def get_user(user_id: int):
    users_dao = UsersDAO(uri=DB_URI)
    user = users_dao.get_user_by_id(user_id)
    return user

@users_router.post("/")
def add_user(user: UserSchema):
    user_for_insert = User(username=user.username, email=user.email, password=user.password, created_at=datetime.now())
    users_dao = UsersDAO(uri=DB_URI)
    user = users_dao.create_user(user_for_insert)
    return user


# but for deleting and updating user must be param id in this functions
@users_router.delete("/{id}")
def delete_user(user_id: int):
    users_dao = UsersDAO(uri=DB_URI)
    user_for_delete = users_dao.get_user_by_id(user_id)
    obj_to_delete = users_dao.delete_user(user_for_delete)
    return obj_to_delete

@users_router.patch("/{id}")
def patch_user(user_id: int, updated_user: UserSchema):
    users_dao = UsersDAO(uri=DB_URI)
    user_to_update = users_dao.patch_user(user_id, updated_user.dict())
    return user_to_update