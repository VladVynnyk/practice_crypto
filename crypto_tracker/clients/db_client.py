from typing import TypeVar

from sqlalchemy.sql.selectable import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from sqlalchemy.exc import ProgrammingError, DatabaseError, NoResultFound, OperationalError, IntegrityError

from ..api.utils import row_to_dict

TModelType = TypeVar("TModelType")
TQueryType = TypeVar("TQueryType")


class DBClient:
    _ERROR_MSG_TEMPLATE: str = 'Failed to {operation} user. Error: {e}'
    _UNEXPECTED_ERROR_MSG_TEMPLATE: str = 'Unexpected error. Failed to {operation} user. Error: {e}'

    def __init__(self, uri: str) -> None:
        self._engine = create_engine(uri)
        self._async_session: sessionmaker[Session] | None = None

    def _get_session(self):
        # self._async_session = scoped_session(sessionmaker(bind=self._engine))
        # return self._async_session
        if not self._async_session:
            self._async_session = scoped_session(sessionmaker(bind=self._engine))
        return self._async_session

    def select_one_object_by_query(self, query: Select) -> TModelType | None:
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                result = session.execute(query)
                row = result.fetchone()
                if row:
                    # print(f"ID: {row[0].id}")
                    # print(f"Ticker: {row[0].ticker}")
                    # print(f"Full name: {row[0].fullName}")
                    # return row_to_dict(row[0])
                    return row[0]

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

    def select_all_objects(self, query: Select) -> TModelType | None:
        print("select all coins in db client")
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                result = session.execute(query)
                rows = result.fetchall()
                objects = []
                if rows:
                    for row in rows:
                        # obj = row_to_dict(row[0])
                        obj = row[0]
                        print(obj)
                        objects.append(obj)
                return objects

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

    # def select_one_object_for_operation(self, query: Select) -> TModelType | None:
    #     sync_session = self._get_session()
    #     try:
    #         with sync_session() as session:
    #             result = session.execute(query)
    #             row = result.fetchone()
    #             if row:
    #                 print("Row: ", row)
    #                 # print(f"ID: {row[0].id}")
    #                 # print(f"Ticker: {row[0].ticker}")
    #                 # print(f"Full name: {row[0].fullName}")
    #                 return row
    #
    #     except (ProgrammingError, DatabaseError) as e:
    #         error_msg = self._ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
    #         # raise SelectOperationError(e, error_msg) from e
    #         raise OperationalError(e, error_msg) from e
    #
    #     except Exception as e:
    #         error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
    #         # raise SelectOperationError(e, error_msg) from e
    #         raise OperationalError(e, error_msg, orig=BaseException()) from e
    #
    #     try:
    #         obj = result.scalars().one()
    #     except NoResultFound:
    #         return None
    #
    #     return obj

    def create_object(self, obj: TModelType) -> TModelType | None:
        sync_session = self._get_session()
        # converted_object_to_dict = row_to_dict(obj)
        # print(converted_object_to_dict)
        print(obj)
        try:
            with sync_session() as session:
                with session.begin():
                    session.add(obj)
        except (ProgrammingError, DatabaseError, IntegrityError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='CREATE', e=e)
            raise OperationalError(e, error_msg, orig=BaseException()) from e
        except Exception as e:
            error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='CREATE', e=e)
            raise OperationalError(e, error_msg, orig=BaseException()) from e

        # return converted_object_to_dict
        # print("Where return: ", obj)
        return {"Success": "Object added"}

    def update_object(self, query: TQueryType) -> TModelType | None:
        sync_session = self._get_session()
        try:
            with sync_session() as session:
                print("Query: ", query)
                result = session.execute(query)
                session.commit()
                print(result)
                row = result.fetchone()
                # return {"Success": "Row is updated"}
                return row[0]

        except (ProgrammingError, DatabaseError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg, orig=BaseException()) from e

        except Exception as e:
            error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='SELECT', e=e)
            # raise SelectOperationError(e, error_msg) from e
            raise OperationalError(e, error_msg, orig=BaseException()) from e

        try:
            coin = result.scalars().one()
        except NoResultFound:
            return None

        return coin

    def delete_object(self, obj: TModelType) -> TModelType | None:
        sync_session = self._get_session()
        print("Object: ", obj)
        try:
            with sync_session() as session:
                with session.begin():
                    session.delete(obj)
                    # return row_to_dict(obj)
                    return obj
        except (ProgrammingError, DatabaseError, IntegrityError) as e:
            error_msg = self._ERROR_MSG_TEMPLATE.format(operation='DELETE', e=e)
            raise OperationalError(e, error_msg, orig=BaseException()) from e
        except Exception as e:
            error_msg = self._UNEXPECTED_ERROR_MSG_TEMPLATE.format(operation='DELETE', e=e)
            raise OperationalError(e, error_msg, orig=BaseException()) from e

    def rollback_operation(self):
        sync_session = self._get_session()
        sync_session.rollback(self)
        return "Rollback operation"
