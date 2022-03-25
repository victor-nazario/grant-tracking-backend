from puller import make_pull
from models import db_session, GrantEntry, init_db
from datetime import datetime
import datetime
from sqlalchemy import select
import constant
import pickle
import unittest
import string
import random


def generate_random_string():
    """
    Creates a random string with 20 characters.
    :return: random string with 20 characters
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(20))
    return random_string


def generate_random_etag():
    """
    This method creates a a random string and stores it in mypickle.pk to be used as an etag.
    """
    file_name = 'mypickle.pk'
    with open(file_name, 'wb') as etag_file:
        # dump your data into the file
        pickle.dump(generate_random_string(), etag_file)


class ModelsTestCase(unittest.TestCase):

    def test_make_pull(self):
        generate_random_etag()
        result = make_pull(constant.RSS_FEED_NEW_OP)
        self.assertTrue(len(result) > 0, "Length of returned list should be greater than 0")
        print(result)
        print(len(result))

    def test_ingestion(self):
        init_db()
        generate_random_etag()
        entry_list = make_pull(constant.RSS_FEED_NEW_OP)
        grant_list = []

        for entry in entry_list:
            grant_list.append(GrantEntry(title=entry['title'], content=entry['content'][0]['value'],
                                         link=entry['link'], close_date=datetime.datetime(2022, 8, 20),
                                         modified=True, etag=''))
        some_session = db_session()
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
        session = db_session()
        result = session.execute(statement).all()
        print(result)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
