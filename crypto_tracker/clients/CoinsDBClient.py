from sqlalchemy.sql.selectable import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from sqlalchemy.exc import ProgrammingError, DatabaseError, NoResultFound, OperationalError

from ..api.utils import row_to_dict
from ..config.database import Coin


class CoinsDBClient:
    _ERROR_MSG_TEMPLATE: str = 'Failed to {operation} user. Error: {e}'
    _UNEXPECTED_ERROR_MSG_TEMPLATE: str = 'Unexpected error. Failed to {operation} user. Error: {e}'

    def _get_session(self):
        self._async_session = scoped_session(sessionmaker(bind=self._engine))
        return self._async_session

    def __init__(self, uri: str) -> None:
        self._engine = create_engine(uri)
        self._async_session: sessionmaker[Session] | None = None

    def select_one_coin_by_query(self, query: Select) -> Coin | None:
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                result = session.execute(query)
                row = result.fetchone()
                if row:
                    print(f"ID: {row[0].id}")
                    print(f"Ticker: {row[0].ticker}")
                    print(f"Full name: {row[0].fullName}")
                    return row_to_dict(row[0])

        except (ProgrammingError, DatabaseError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg) from e

        except Exception as e:
            error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg, orig=BaseException()) from e

        try:
            coin = result.scalars().one()
        except NoResultFound:
            return None

        return coin

    def select_all_coins(self, query: Select) -> Coin | None:
        print("select all coins in db client")
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                result = session.execute(query)
                rows = result.fetchall()
                coins = []
                if rows:
                    for row in rows:
                        coin = {
                            "id": row[0].id,
                            "ticker": row[0].ticker,
                            "fullName": row[0].fullName
                        }
                        print(f"ID: {row[0].id}")
                        print(f"Ticker: {row[0].ticker}")
                        print(f"Full name: {row[0].fullName}")
                        coins.append(coin)
                # rows = result.fetchall()
                # print(rows)
                return coins

        except (ProgrammingError, DatabaseError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg) from e

        except Exception as e:
            error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg, orig=BaseException()) from e

        try:
            coin = result.scalars().one()
        except NoResultFound:
            return None

        return coin

    def update_coin(self, updated_coin: Coin) -> Coin | None:
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                session.add(updated_coin)
                session.commit()
        except (ProgrammingError, DatabaseError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='UPDATE', e=e)
            raise OperationalError(e, error_msg, orig=BaseException())
        return updated_coin

    def delete_coin(self) -> Coin | None:
        pass