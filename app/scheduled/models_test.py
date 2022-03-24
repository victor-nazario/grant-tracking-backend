import unittest
from datetime import datetime
import datetime
from sqlalchemy import select
from models import GrantEntry, db_session, init_db


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.model1 = GrantEntry(title='', content='', link='',  close_date=datetime.datetime(2022, 8, 20),
                                 modified=True, etag='')
        self.model2 = GrantEntry(title='', content='', link='', close_date=datetime.datetime(2022, 1, 12),
                                 modified=False, etag='')

    def test_accepts_submission(self):
        self.assertTrue(self.model1.accepts_submission)
        self.assertFalse(self.model2.accepts_submission, "Present date exceeds closed date.")
        self.assertFalse(self.model2.accepts_submission)
        self.assertTrue(self.model1.accepts_submission, "Present date doesn't exceeds closed date.")

    def test_isModified(self):
        self.assertTrue(self.model1.is_modified)
        self.assertFalse(self.model2.is_modified, "Can't be modify.")
        self.assertFalse(self.model2.is_modified)
        self.assertTrue(self.model1.is_modified, "Can be modify.")

    # def test_session(self):
    #     init_db()
    #     some_session = db_session()
    #     with some_session as session:
    #         session.add(GrantEntry(title='Title8', content='Some content', link='test8.com',
    #                                close_date=datetime.datetime(2022, 8, 20), modified=True, etag='dsfasd'))
    #         session.commit()
    #     statement = select(GrantEntry.title)
    #     result = session.execute(statement).all()
    #     print(result)


if __name__ == '__main__':
    unittest.main()
