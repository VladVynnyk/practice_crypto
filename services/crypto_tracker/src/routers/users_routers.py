import secrets
import sys

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from typing_extensions import Annotated

sys.path.append("../../..")
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from services.crypto_tracker.src.daos.users_dao import UsersDAO
from services.crypto_tracker.src.settings import get_settings

# It's will be temporary imports
from services.crypto_tracker.src.database import User
from services.crypto_tracker.src.models import UserSchema, UserSchemaRegister

DB_URI = get_settings().db_uri

security = HTTPBasic()


# def get_current_username(
#         credentials: Annotated[HTTPBasicCredentials, Depends(security)]
# ):
#     current_username_bytes = credentials.username.encode("utf8")
#     correct_username_bytes = b"stanleyjobson"
#     is_correct_username = secrets.compare_digest(
#         current_username_bytes, correct_username_bytes
#     )
#     current_password_bytes = credentials.password.encode("utf8")
#     correct_password_bytes = b"swordfish"
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username


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

    response = {"username": user[0].username, "email": user[0].email, "password": user[0].password,
                "created_at": user[0].created_at}
    return response


@users_router.post("/")
def add_user(user: UserSchemaRegister):
    # also in this endpoint must be check if user is not repeated
    if user.password == user.confirmed_password:
        user_for_insert = User(username=user.username, email=user.email, password=user.password,
                               created_at=datetime.now())
        users_dao = UsersDAO(uri=DB_URI)
        user = users_dao.create_user(user_for_insert)
        return user
    else:
        return {"message": "Your password is not correct. Please, try to register again."}


@users_router.post("/log_in")
def log_in_for_user(user: UserSchema):
    # logic: 1) we are checking in database for user with specific username
    # 2) we are finding this user with username and checking his password
    # 3) if password isn't correct or username not found we must return message about error
    users_dao = UsersDAO(uri=DB_URI)
    user_from_db = users_dao.get_user_by_username(user.username)
    if user_from_db:
        if user_from_db.password == user.password:
            return user_from_db
        else:
            return {"message": "Username or password isn't correct"}
    else:
        return {"message": "Username or password isn't correct"}


# @users_router.get("/me")
# def read_current_user(username: Annotated[str, Depends(get_current_username)]):
#     return {"username": username}


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
