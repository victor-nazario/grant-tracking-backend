from app.scheduled.layers.models import GrantEntry
from app.session_generator.create_session import get_session
from app.scheduled.layers.processing import obtain_close_date
from datetime import date
from dateutil.relativedelta import relativedelta


def create_grants_from_entries(entry_list: list, is_modified: bool):
    """
    Creates a list of GrantEntry objects from a list of entries. Each entry contains the title,
    the content, and the link for each grant.
    :param is_modified: if the entry_list contains modified entries or not
    :return list of GrantEntry objects
    :param entry_list: list
    """
    grant_list = []

    for entry in entry_list:
        entry_content = entry['content'][0]['value']
        close_date = obtain_close_date(entry_content)
        if close_date is None:
            close_date = date.today() + relativedelta(months=6)

        grant_list.append(GrantEntry(title=entry['title'], content=entry_content,
                                     link=entry['link'], close_date=close_date,
                                     modified=is_modified, etag=entry['etag']))

    return grant_list


def insert_grants(grant_list: list):
    """
    Inserts a list of GrantEntry objects into the database.
    :param grant_list: list
    """
    some_session = get_session()
    with some_session as session:
        session.add_all(grant_list)
        session.commit()
