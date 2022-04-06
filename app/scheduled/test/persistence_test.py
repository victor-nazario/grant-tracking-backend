import unittest
from app.scheduled.layers.persistence import create_grants_from_entries, insert_grants
from app.scheduled.layers import constant
from app.scheduled.layers.puller import make_pull
from sqlalchemy.engine import ChunkedIteratorResult
from test_utils import generate_random_etag
from sqlalchemy import select
from app.scheduled.layers.models import GrantEntry, init_db
from app.session_generator.create_session import get_session


class PersistenceTestCase(unittest.TestCase):

    def test_convert_to_grant(self):
        generate_random_etag()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP)
        grant_list = create_grants_from_entries(entry_list, False)
        self.assertTrue(len(entry_list) == len(grant_list))
        print(grant_list)

    '''This test may return an error if make_pull has a connection_error or a 304 return status.
    We have to make sure to catch this error.'''
    def test_insert_grants(self):
        init_db()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP, generate_random_etag())
        grant_list = create_grants_from_entries(entry_list, False)
        insert_grants(grant_list)
        session = get_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement).all()
        session.close()
        self.assertTrue(len(result) > 0)
        print(result)

    def test_closing_session(self):
        session = get_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        session.close()
        session = get_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement)
        print(result)
        self.assertIsInstance(result, ChunkedIteratorResult)


