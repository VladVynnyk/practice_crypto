import sys
sys.path.append("..")
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.exc import DatabaseError

from crypto_tracker.config.settings import get_settings


class DBClient:
    _scoped_session = None

    def execute_query_one(self, query):
        scoped_session = self._get_scoped_session()
        with scoped_session() as session:
            result = session.execute(query)
            # users = session.query(User).all()
            return result.get_one()

    def execute_query_many(self, query):
        scoped_session = self._get_scoped_session()
        with scoped_session() as session:
            result = session.execute(query)
            # users = session.query(User).all()
            return result.get_many()

    def _get_scoped_session(self) -> Session:
        if not self._scoped_session:
            self._scoped_session = scoped_session(
                sessionmaker(bind=create_engine(get_settings().db_uri))
            )
        return self._scoped_session
