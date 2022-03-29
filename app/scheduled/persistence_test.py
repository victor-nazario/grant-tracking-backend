import unittest
from persistence import create_grants_from_entries, insert_grants
import constant
from puller import make_pull
from test_utils import generate_random_etag
from sqlalchemy import select
from models import GrantEntry, db_session, init_db


class PersistenceTestCase(unittest.TestCase):

    def test_convert_to_grant(self):
        generate_random_etag()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP)
        grant_list = create_grants_from_entries(entry_list, False)
        self.assertTrue(len(entry_list) == len(grant_list))
        print(grant_list)
        return grant_list

    '''This test may return an error if make_pull has a connection_error or a 304 return status.
    We have to make sure catch this error.'''
    def test_insert_grants(self):
        init_db()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP, generate_random_etag())
        grant_list = create_grants_from_entries(entry_list, False)
        insert_grants(grant_list)
        session = db_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        print(result)

