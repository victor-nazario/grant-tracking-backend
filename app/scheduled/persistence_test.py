import unittest
from persistence import convert_to_grant
import constant
from puller import make_pull
from test_utils import generate_random_etag
from sqlalchemy import select
from models import GrantEntry, db_session


class PersistenceTestCase(unittest.TestCase):

    def test_convert_to_grant(self):
        generate_random_etag()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP)
        grant_list = convert_to_grant(entry_list)
        self.assertTrue(len(entry_list) == len(grant_list))
        print(grant_list)

    def test_select_grant_date(self):
        session = db_session()
        statement = select(GrantEntry.close_date)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        print(result)

