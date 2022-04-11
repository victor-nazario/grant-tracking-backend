import unittest

from app.session_generator.create_session import get_session

from app.scheduled.layers.deletion import delete_grant
from app.scheduled.layers.models import GrantEntry
from datetime import datetime
import datetime


class DeletionTestCase(unittest.TestCase):

    def test_deletion(self):
        session = get_session()
        session.add(GrantEntry(title="Monday", content="ehfjkewhfkjewhjkeh448", link="www.grant1.com",
                               close_date=1634779424, etag="", modified=True, opp_num=1))
        session.add(GrantEntry(title="Tuesday", content="sasasasasasasa", link="www.grant2.com",
                               close_date=1642037024, etag="", modified=True, opp_num=1))
        session.add(GrantEntry(title="Wednesday", content="rererererererere", link="www.grant3.com",
                               close_date=1647393824, etag="", modified=True, opp_num=1))
        session.add(GrantEntry(title="Thursday", content="rererererererere", link="www.grant4.com",
                               close_date=1773624224, etag="", modified=True, opp_num=1))

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
