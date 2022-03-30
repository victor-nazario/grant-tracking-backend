from puller import make_pull
from models import db_session, GrantEntry, init_db, get_session
from datetime import datetime, date
from sqlalchemy import select
from test_utils import generate_random_string, generate_random_etag
import constant
import pickle
import unittest


class ModelsTestCase(unittest.TestCase):

    def test_make_pull(self):
        result = make_pull(constant.RSS_FEED_NEW_OP, generate_random_etag())
        self.assertTrue(len(result) > 0, "Length of returned list should be greater than 0")
        print(result)
        print(len(result))

    def test_ingestion(self):
        init_db()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP, generate_random_etag())
        grant_list = []

        for entry in entry_list:
            grant_list.append(GrantEntry(title=entry['title'], content=entry['content'][0]['value'],
                                         link=entry['link'], close_date=date(2022, 8, 20),
                                         modified=True, etag=''))
        some_session = get_session()
        with some_session as session:
            session.add_all(grant_list)
            session.commit()
        statement = select(GrantEntry.title)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        print(result)

    '''Make sure the db contains data before running. 
    Run test_ingestion if db is empty'''
    def test_select_all_grant_titles(self):
        statement = select(GrantEntry.title, GrantEntry.content, GrantEntry.link)
        session = get_session()
        result = session.execute(statement).all()
        session.close()
        print(result)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
