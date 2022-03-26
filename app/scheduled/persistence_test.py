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
        grant_list = create_grants_from_entries(entry_list)
        self.assertTrue(len(entry_list) == len(grant_list))
        print(grant_list)
        return grant_list

    def test_insert_grants(self):
        init_db()
        generate_random_etag()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP)
        grant_list = create_grants_from_entries(entry_list)
        insert_grants(grant_list)
        session = db_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        print(result)

