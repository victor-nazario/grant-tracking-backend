from puller import make_pull
from models import db_session, GrantEntry, init_db
from datetime import datetime
import datetime
from sqlalchemy import select
import constant
import pickle
import unittest


class ModelsTestCase(unittest.TestCase):

    def test_make_pull(self):
        assert len(make_pull(constant.RSS_FEED_NEW_OP)['title'][0]) > 0, "Length of returned list should be greater than 0"


    def test_ingestion(self):
        file_name = 'mypickle.pk'
        with open(file_name, 'wb') as etag_file:
            # dump your data into the file
            pickle.dump('75679f-5defe30v79e6k', etag_file)
        data = make_pull(constant.RSS_FEED_NEW_OP)
        list_titles = data['title']
        list_contents = data['content']
        list_links = data['link']
        list_grants = []
        for i in range(len(list_titles)):
            list_grants.append(GrantEntry(title=list_titles[i], content=list_contents[i][0]['value'],
                                          link=list_links[i], close_date=datetime.datetime(2022, 8, 20),
                                          modified=True, etag=''))
        some_session = db_session()
        with some_session as session:
            session.add_all(list_grants)
            session.commit()
        statement = select(GrantEntry.title)
        result = session.execute(statement).all()
        self.assertTrue(len(result) > 0)
        print(result)

    def test_select_all_grant_titles(self):
        statement = select(GrantEntry.title)
        session = db_session()
        print(session.execute(statement).all())


if __name__ == '__main__':
    unittest.main()
