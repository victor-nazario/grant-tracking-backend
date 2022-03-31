from app.scheduled.models import GrantEntry, get_session
from datetime import datetime


def delete_grant():
    session = get_session()
    session.query(GrantEntry).filter(datetime.utcnow() > GrantEntry.close_date).delete()
    session.commit()
