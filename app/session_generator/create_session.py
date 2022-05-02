from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database


db_settings = {
    'DATABASE_URI': 'postgresql+psycopg2://root:root@db:5432/test_db',
    'DATABASE_CONNECT_OPTIONS': ''
}


def get_engine(uri: str):
    """
    Checks if database exist before creating a new engine.
    The function receives the database uri as an argument to create the engine.
    :param uri: str containing the database’s uri
    :return: a new engine
    """
    if not database_exists(uri):
        create_database(uri)
    new_engine = create_engine(uri, pool_size=50, echo=False, echo_pool=False)
    return new_engine


def get_session():
    """
    This function creates new sessions after checking if the database exists by calling the function
    get_engine which returns a new engine to be used by the new session.
    :return: a new session
    """
    new_engine = get_engine(db_settings['DATABASE_URI'])
    session = sessionmaker(bind=new_engine)()
    return session
