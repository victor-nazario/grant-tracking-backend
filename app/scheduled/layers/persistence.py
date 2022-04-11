from app.scheduled.layers.models import GrantEntry
from app.session_generator.create_session import get_session
from app.scheduled.layers.processing import obtain_close_date
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.dialects.postgresql import insert


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
        # If we cannot parse a date, we will give the grant a 6 months grace period.
        if close_date is None:
            future_date = date.today() + relativedelta(months=6)
            dt = datetime.combine(future_date, datetime.min.time())
            close_date = int(dt.timestamp())

        grant_list.append(GrantEntry(title=entry['title'], opp_num=entry['opp_num'],
                                     content=entry_content, link=entry['link'],
                                     close_date=close_date, modified=is_modified,
                                     etag=entry['etag']))

    return grant_list


def insert_grants_if_unique(grant_list: list):
    """
    Insert grants in database if their opportunity number does not exist already in the database,
    otherwise, updates de current grant with the new data. The function calls the private function
    _insert_modified_grants, if the list grant_list contains a list of modified grants. This is,
    if the modified property is 'True'. If the modified property is 'False', the _insert_new_grants
    function will be called.
    :param grant_list: list of GrantEntry objects
    """
    # if grant is modified
    if grant_list[0].modified:
        _insert_modified_grants(grant_list)
    else:
        _insert_new_grants(grant_list)


def _insert_modified_grants(grant_list: list):
    """
    This functions is called from the insert_grants_if_unique function. It inserts or updates
    grants from the modified RSS feed. Also, updates the modified property to true for grants already
    in the database if the property if set to 'False'.
    :param grant_list: list og GrantEntry objects
    """
    session = get_session()
    for grant in grant_list:
        insert_stmt = insert(GrantEntry).values(
            title=grant.title,
            opp_num=grant.opp_num,
            content=grant.content,
            link=grant.link,
            close_date=grant.close_date,
            modified=grant.modified,
            etag=grant.etag
        )

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='entries_opp_num_key',
            set_=dict(
                title=grant.title,
                opp_num=grant.opp_num,
                content=grant.content,
                link=grant.link,
                close_date=grant.close_date,
                modified=grant.modified,
                etag=grant.etag
            )
        )
        session.execute(do_update_stmt)

    session.commit()
    session.close()


def _insert_new_grants(grant_list: list):
    """
    This functions is called from the insert_grants_if_unique function. It inserts or updates
    grants from the New RSS feed into the database.
    :param grant_list: list of GrantEntry objects
    """
    session = get_session()
    for grant in grant_list:
        insert_stmt = insert(GrantEntry).values(
            title=grant.title,
            opp_num=grant.opp_num,
            content=grant.content,
            link=grant.link,
            close_date=grant.close_date,
            modified=grant.modified,
            etag=grant.etag
        )

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='entries_opp_num_key',
            set_=dict(
                title=grant.title,
                opp_num=grant.opp_num,
                content=grant.content,
                link=grant.link,
                close_date=grant.close_date,
                etag=grant.etag
            )
        )
        session.execute(do_update_stmt)

    session.commit()
    session.close()
