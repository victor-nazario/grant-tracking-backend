from app.scheduled.layers.models import GrantEntry
from app.session_generator.create_session import get_session
from app.scheduled.layers.processing import obtain_close_date
from datetime import date
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
        if close_date is None:
            close_date = date.today() + relativedelta(months=6)

        grant_list.append(GrantEntry(title=entry['title'], opp_num=entry['opp_num'],
                                     content=entry_content, link=entry['link'],
                                     close_date=close_date, modified=is_modified,
                                     etag=entry['etag']))

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


def insert_grants_if_unique(grant_list: list):
    if grant_list[0].modified:
        _insert_modified_grants(grant_list)
    else:
        _insert_new_grants(grant_list)


def _insert_modified_grants(grant_list: list):
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
                # modified=grant.modified,
                etag=grant.etag
            )
        )
        session.execute(do_update_stmt)

    session.commit()
    session.close()
