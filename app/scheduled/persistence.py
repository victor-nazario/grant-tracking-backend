from models import db_session, GrantEntry, init_db
from processing import obtain_close_date
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def create_grants_from_entries(entry_list: list):
    """
    Creates a list of GrantEntry objects from a list of entries. Each entry contains the title,
    the content, and the link for each grant.
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
                                     link=entry['link'], close_date=close_date.strftime('%b %d, %Y'),
                                     modified=True, etag=''))

    return grant_list
