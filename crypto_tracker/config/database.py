# from sqlalchemy import create_engine
#
# engine = create_engine('postgresql+psycopg2://postgres:postgres\@hostname/database_name')


import sqlalchemy
from typing import List
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from sqlalchemy.orm import Session

db_user = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '49153'
db_name = 'cryptodb'

# create the database url for SQLAlchemy
# db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# engine = sqlalchemy.create_engine(db_url)
# connection = engine.connect()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=False)
    created_at = Column(DateTime, unique=False)
    portfolio: Mapped[List["Portfolio"]] = relationship()


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name = Column(String, unique=False)
    created_at = Column(DateTime, unique=False)
    portfolioCoin: Mapped[List["PortfolioCoin"]] = relationship()
    transaction: Mapped[List["Transaction"]] = relationship()


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True)
    fullName = Column(String, unique=True)
    transaction: Mapped[List["Transaction"]] = relationship()


class PortfolioCoin(Base):
    __tablename__ = "portfolio_coin"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    coin_id: Mapped[int] = mapped_column(ForeignKey("coin.id"))
    amount = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    coin_id: Mapped[int] = mapped_column(ForeignKey("coin.id"))
    transaction_type = Column(String, unique=False)
    amount = Column(Float, unique=False)
    price = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False)