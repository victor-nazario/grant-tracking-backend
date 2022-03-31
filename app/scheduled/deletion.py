from app.scheduled.models import GrantEntry, get_session
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s-%(message)s')
"""
Delete grant from database if present date time exceeds the close date of the grant.
"""


def delete_grant():
    session = get_session()
    session.query(GrantEntry).filter(datetime.utcnow() > GrantEntry.close_date).delete()
    session.commit()
    logging.info('Ran deletion layer')
