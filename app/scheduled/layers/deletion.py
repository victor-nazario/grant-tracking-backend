from app.scheduled.layers.models import GrantEntry
from app.session_generator.create_session import get_session
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s-%(message)s')
"""
Delete grant from database if present date time exceeds the close date of the grant.
"""


def delete_grant():
    session = get_session()
    session.query(GrantEntry).filter(int(datetime.utcnow().timestamp()) > GrantEntry.close_date).delete()
    session.commit()
    session.close()
