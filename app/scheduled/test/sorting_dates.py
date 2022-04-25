import unittest

from app.session_generator.create_session import get_session

from app.scheduled.layers.deletion import delete_grant
from app.scheduled.layers.models import GrantEntry
from datetime import datetime
import datetime


class SortingTestCase(unittest.TestCase):

    def test_sorting_dates(self):
        session = get_session()
        session.add(GrantEntry(title="Monday", content="ehfjkewhfkjewhjkeh448", link="www.grant1.com",
                               close_date=1634779424, etag="", modified=True, opp_num=2))
        session.add(GrantEntry(title="Tuesday", content="sasasasasasasa", link="www.grant2.com",
                               close_date=1642037024, etag="", modified=True, opp_num=3))
        session.add(GrantEntry(title="Wednesday", content="rererererererere", link="www.grant3.com",
                               close_date=1647393824, etag="", modified=True, opp_num=4))
        session.add(GrantEntry(title="Thursday", content="rererererererere", link="www.grant4.com",
                               close_date=1773624224, etag="", modified=True, opp_num=5))
        session.add(GrantEntry(title="Friday", content="jfsdkhhjdhfkjdsh", link="www.grant5.com",
                               close_date=1990192765, etag="", modified=True, opp_num=6))

        session.commit()
        session.close()
