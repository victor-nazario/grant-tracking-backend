import unittest
from app.scheduled.layers.persistence import create_grants_from_entries, insert_grants, insert_grants_if_unique
from app.scheduled.layers import constant
from app.scheduled.layers.puller import make_pull
from sqlalchemy.engine import ChunkedIteratorResult
from test_utils import generate_random_etag, generate_random_string, create_grant_objects
from sqlalchemy import select
from app.scheduled.layers.models import GrantEntry, init_db
from app.session_generator.create_session import get_session
from datetime import date



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

    def test_insert_if_unique(self):
        init_db()
        random_etag = generate_random_string(20)
        entry_list = make_pull(constant.RSS_FEED_NEW_OP, '')
        grant_list = []
        for entry in entry_list:
            grant_list.append(GrantEntry(title=entry['title'], opp_num=entry['opp_num'],
                                         content=entry['content'][0]['value'], link=entry['link'],
                                         close_date=date(2022, 8, 20), modified=False,
                                         etag=random_etag))
        insert_grants_if_unique(grant_list)
        grant_list_size = len(grant_list)
        session = get_session()
        inserted_list1 = session.execute(select(GrantEntry.etag)).all()
        inserted_size = len(inserted_list1)
        print("Inserted size: " + str(inserted_size))
        print("grant_list_size: " + str(grant_list_size))
        self.assertTrue(grant_list_size == inserted_size)
        first_etag = inserted_list1[0][0]

        random_etag2 = generate_random_string(20)
        entry_list = make_pull(constant.RSS_FEED_NEW_OP, first_etag)
        grant_list = []
        for entry in entry_list:
            grant_list.append(GrantEntry(title=entry['title'], opp_num=entry['opp_num'],
                                         content=entry['content'][0]['value'], link=entry['link'],
                                         close_date=date(2022, 8, 20), modified=False,
                                         etag=random_etag2))
        insert_grants_if_unique(grant_list)
        inserted_list2 = session.execute(select(GrantEntry.etag)).all()
        inserted_size2 = len(inserted_list2)
        self.assertTrue(inserted_size2 == inserted_size)
        second_etag = inserted_list2[0][0]
        print("First Etag = " + first_etag)
        print("Second Etag = " + second_etag)
        self.assertFalse(first_etag == second_etag)
        return second_etag

    def test_insert_if_modified(self):
        result = create_grant_objects(constant.RSS_FEED_NEW_OP, '', False)
        grant_list = result[0]
        previous_etag = result[1]
        insert_grants_if_unique(grant_list)
        result = create_grant_objects(constant.RSS_FEED_NEW_OP, previous_etag, True)
        grant_list = result[0]
        previous_etag = result[1]
        insert_grants_if_unique(grant_list)
        result = create_grant_objects(constant.RSS_FEED_NEW_OP, previous_etag, False)
        grant_list = result[0]
        insert_grants_if_unique(grant_list)
        session = get_session()
        modified_list = session.execute(select(GrantEntry.modified)).all()
        for modified in modified_list:
            self.assertTrue(modified[0])

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


