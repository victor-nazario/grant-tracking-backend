import feedparser
import sqlalchemy.exc
from sqlalchemy import desc
import logging
import constant
from models import db_session, GrantEntry
from puller import make_pull
from persistence import create_grants_from_entries, insert_grants



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s-%(message)s')


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
        except AttributeError:
            print("had err")
            last_new_entry = ''
            last_mod_entry = ''

    _pull_and_persist(constant.RSS_FEED_NEW_OP, last_new_entry, False)
    _pull_and_persist(constant.RSS_FEED_MOD_OP, last_mod_entry, True)


def _pull_and_persist(url: str, last_etag: str, is_modified: bool):
    """
    This function is called from initiate_pull_and_process_layers to pull and persist the data
    for each RSS Feed.
    :param url: string containing the url for the RSS Feed
    :param last_etag: the last etag stored in the database for a specific feed
    :param is_modified: True for modified grants, False otherwise
    """
    entry_list = make_pull(url, last_etag)
    feed_type = "MODIFIED" if is_modified else "NEW"
    if entry_list == 304:
        print('\n')
        logging.info('Status 304: RSS feed is the same for ' + feed_type + ' opportunities')
    elif len(entry_list) == 0:
        print('\n')
        logging.info('Could not connect to ' + feed_type + ' opportunities RSS feed')
    else:
        grant_list = create_grants_from_entries(entry_list, is_modified)
        insert_grants(grant_list)
