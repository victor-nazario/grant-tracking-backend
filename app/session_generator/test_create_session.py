import unittest
from create_session import get_engine, get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.scheduled.layers.models import init_db

url = 'postgresql+psycopg2://root:root@localhost:5432/test_create_session_db'


class PersistenceTestCase(unittest.TestCase):

    def test_get_engine(self):
        new_engine = get_engine(url)
        self.assertTrue(new_engine)
