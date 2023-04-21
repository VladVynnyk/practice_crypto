from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crypto_tracker.config.database import User


# Function for insert data into table "user"
def insert_data_to_user_table():
    date = datetime.now()
    users = [
        User(username="some username", email="email@example.com", password="some pass", created_at=date),
        User(username="some username2", email="email2@example.com", password="some pass2", created_at=date)
    ]
    session_maker = sessionmaker(bind=create_engine('postgresql+psycopg2://postgres:1234@localhost:49153/cryptodb'))
    with session_maker as session:
        for user in users:
            session.add(user)
        session.commit()

    return user


# Function for converting SQLAlchemy row to dict
def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
