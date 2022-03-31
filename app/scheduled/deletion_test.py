import unittest

from models import GrantEntry, init_db, get_session

from app.scheduled.deletion import delete_grant
from app.scheduled.models import GrantEntry
from datetime import datetime
import datetime


class DeletionTestCase(unittest.TestCase):

    def test_deletion(self):
        session = get_session()
        session.add(GrantEntry(title="Monday", content="ehfjkewhfkjewhjkeh448", link="www.grant1.com",
                               close_date=datetime.datetime(2021, 10, 20), etag="", modified=True))
        session.add(GrantEntry(title="Tuesday", content="sasasasasasasa", link="www.grant2.com",
                               close_date=datetime.datetime(2022, 1, 12), etag="", modified=True))
        session.add(GrantEntry(title="Wednesday", content="rererererererere", link="www.grant3.com",
                               close_date=datetime.datetime(2022, 3, 15), etag="", modified=True))
        session.add(GrantEntry(title="Thursday", content="rererererererere", link="www.grant4.com",
                               close_date=datetime.datetime(2026, 10, 7), etag="", modified=True))

        session.commit()
        before_delete = session.query(GrantEntry).count()
        print("Before Delete:")
        print(before_delete)
        session.close()
        delete_grant()

        after_delete = session.query(GrantEntry).count()
        print("After Delete:")
        print(after_delete)
        self.assertTrue((before_delete - 3) == after_delete)
