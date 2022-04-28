import unittest
from create_session import get_engine, get_session

url = 'postgresql+psycopg2://root:root@localhost:5432/test_create_session_db'


class PersistenceTestCase(unittest.TestCase):

    def test_get_engine(self):
        new_engine = get_engine(url)
        self.assertTrue(new_engine)