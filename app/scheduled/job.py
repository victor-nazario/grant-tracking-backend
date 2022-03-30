import feedparser
import sqlalchemy.exc
from sqlalchemy import desc

import constant
from models import db_session, GrantEntry
from puller import make_pull


def initiate_pull_and_process_layers():
    """
    This is the function that orchestrates and manages all scheduled jobs (such as pulling, processing,
    persistence, etc) and will be run a given amount of times per day.
    """
    feedparser.USER_AGENT = constant.USER_AGENT
    session_from_model = db_session()
    with session_from_model as session:
        try:
            last_new_entry = session.query(GrantEntry).filter_by(modified=False).order_by(desc('id')).first().etag
            last_mod_entry = session.query(GrantEntry).filter_by(modified=True).order_by(desc('id')).first().etag
        except sqlalchemy.exc.ProgrammingError:
            print("had err")
            last_new_entry = ''
            last_mod_entry = ''

    print(len(make_pull(constant.RSS_FEED_NEW_OP, last_new_entry)))
    print(len(make_pull(constant.RSS_FEED_MOD_OP, last_mod_entry)))
