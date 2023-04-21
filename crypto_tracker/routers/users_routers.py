import sys
sys.path.append("..")
from fastapi import APIRouter
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crypto_tracker.daos.users_dao import UsersDAO
# from .daos.users_dao import UsersDAO
from crypto_tracker.config.settings import get_settings

#It's will be temporary imports
from crypto_tracker.config.database import User
from crypto_tracker.api.models.pydantic_models.models import UserSchema

Db_uri = get_settings().db_uri

users_router = APIRouter(
    prefix="/users",
)

#CRUD for "user" table
@users_router.get("/")
def get_users():
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        users = session.query(User).all()
        return users
    # users_dao = UsersDAO()
    # users = users_dao.get_all_users()
    # return users

@users_router.get("/{id}")
def get_user(id):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        user = session.query(User).where(User.id==id).first()
        return user


@users_router.post("/")
def add_user(user: UserSchema):
    user_for_insert = User(username=user.username, email=user.email, password=user.password, created_at=datetime.now())
    print(user_for_insert)
    print(Db_uri)
    Session = scoped_session(sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.add(user_for_insert)
        session.commit()
    return user


#but for deleting and updating user must be param id in this functions
@users_router.delete("/{id}")
def delete_user(id:int):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        query = session.query(User).where(User.id == id)
        user = query.first()
        if not user:
            return {"message": "User not found"}
        session.delete(user)
        session.commit()
    return {"message": "User deleted"}

@users_router.patch("/{id}")
def patch_user(id: int, user: UserSchema):
    Session = scoped_session(
        sessionmaker(bind=create_engine(Db_uri)))
    with Session() as session:
        session.query(User).where(User.id == id).update(user.dict())
        session.commit()
    return user