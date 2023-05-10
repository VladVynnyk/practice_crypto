from unittest.mock import MagicMock, Mock, patch

import pytest
from sqlalchemy.exc import DatabaseError
from fastapi.testclient import TestClient

from services.crypto_tracker.main import app

from services.crypto_tracker.src.clients.db_client import DBClient
from services.crypto_tracker.src.settings import get_settings


class TestDBClient:

    client = TestClient(app=app)
    DB_URI = get_settings().db_uri

    def test_database_error_in_select_one_object_by_query(self):
        # query = "Select * from table where id = 1"
        # with pytest.raises(DatabaseError) as e:
        #     db_client = DBClient(self.DB_URI)
        #     db_client.select_one_object_by_query('foo')
        #
        # assert "non existing table" in str(e.value)
        pass