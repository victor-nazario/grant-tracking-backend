from app.scheduled.models import db_session, GrantEntry
from datetime import datetime


def delete_grant():
    session = db_session()
    session.query(GrantEntry).filter(datetime.utcnow() > GrantEntry.close_date).delete()
    session.commit()
