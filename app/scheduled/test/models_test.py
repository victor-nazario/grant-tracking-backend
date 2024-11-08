import unittest
from datetime import datetime
import datetime
from sqlalchemy import select
from app.scheduled.layers.models import GrantEntry, init_db
from app.session_generator import create_session


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.model1 = GrantEntry(title='', content='', link='',  close_date=1712883953,
                                 modified=True, etag='', opp_num=1)
        self.model2 = GrantEntry(title='', content='', link='', close_date=1649516869,
                                 modified=False, etag='', opp_num=1)

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

    def test_session(self):
        init_db()
        some_session = create_session.get_session()
        with some_session as session:
            session.add(GrantEntry(title='Titl1', content='Some content', link='test11.com',
                                   close_date=1649516839, modified=True, etag='dsfasd', opp_num=1))
            session.commit()
        statement = select(GrantEntry.title)
        result = session.execute(statement).all()
        print(result)


if __name__ == '__main__':
    unittest.main()
