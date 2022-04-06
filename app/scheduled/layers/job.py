import feedparser
import sqlalchemy.exc
from sqlalchemy import desc
import logging
import app.scheduled.layers.constant as constant
from app.scheduled.layers.models import GrantEntry
from app.session_generator.create_session import get_session
from app.scheduled.layers.puller import make_pull
from app.scheduled.layers.persistence import create_grants_from_entries, insert_grants, insert_grants_if_unique


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s-%(message)s')


def initiate_pull_and_process_layers():
    """
    This is the function that orchestrates and manages all scheduled jobs (such as pulling, processing,
    persistence, etc) and will be run a given amount of times per day.
    """
    feedparser.USER_AGENT = constant.USER_AGENT
    session_from_model = get_session()
    with session_from_model as session:
        try:
            last_new_entry = session.query(GrantEntry).filter_by(modified=False).order_by(desc('id')).first().etag
        except sqlalchemy.exc.ProgrammingError:
            logging.info('Entered PROGRAMMING error handling NEW feed')
            last_new_entry = ''
        except AttributeError:
            logging.info('Entered ATTRIBUTE error handling NEW feed')
            last_new_entry = ''

        try:
            last_mod_entry = session.query(GrantEntry).filter_by(modified=True).order_by(desc('id')).first().etag
        except sqlalchemy.exc.ProgrammingError:
            logging.info('Entered PROGRAMMING error handling for MODIFIED feed')
            last_mod_entry = ''
        except AttributeError:
            logging.info('Entered ATTRIBUTE error handling MODIFIED feed')
            last_mod_entry = ''

    result = False
    while not result:
        result = _pull_and_persist(constant.RSS_FEED_NEW_OP, last_new_entry, False)

    result = False
    while not result:
        result = _pull_and_persist(constant.RSS_FEED_MOD_OP, last_mod_entry, True)


def _pull_and_persist(url: str, last_etag: str, is_modified: bool):
    """
    This function is called from initiate_pull_and_process_layers to pull and persist the data
    for each RSS Feed.
    :param url: string containing the url for the RSS Feed
    :param last_etag: the last etag stored in the database for a specific feed
    :param is_modified: True for modified api, False otherwise
    """
    entry_list = make_pull(url, last_etag)
    feed_type = "MODIFIED" if is_modified else "NEW"
    if entry_list == 304:
        print('\n')
        logging.info('Status 304: RSS feed is the same for ' + feed_type + ' opportunities')
        return True
    elif len(entry_list) == 0:
        print('\n')
        logging.info('Could not connect to ' + feed_type + ' opportunities RSS feed')
        return False
    else:
        grant_list = create_grants_from_entries(entry_list, is_modified)
        insert_grants_if_unique(grant_list)
        logging.info('Inserted ' + feed_type + ' api into database')
        return True
