from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import psycopg2
from sqlalchemy_utils import database_exists, create_database



db_settings = {
    'DATABASE_URI': 'postgresql+psycopg2://root:root@localhost:5432/test_db',
    'DATABASE_CONNECT_OPTIONS': ''
}

Base = declarative_base()

engine = create_engine(db_settings['DATABASE_URI'], convert_unicode=True, echo=True)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def _get_engine(uri: str):
    """
    Checks if database exist before creating a new engine.
    The function receives the database uri as an argument to create the engine.
    :param uri: string
    :return: a new engine
    """
    url = uri
    if not database_exists(url):
        create_database(url, 'entries')
    new_engine = create_engine(url, pool_size=50, echo=False)
    return new_engine


def get_session():
    """
    This function creates new sessions after checking if the database exist by calling the function
    _get_engine which returns a new engine to be used by the new session
    :return: a new session
    """
    new_engine = _get_engine(db_settings['DATABASE_URI'])
    session = sessionmaker(bind=new_engine)()
    return session


def init_db():
    Base.metadata.create_all(bind=_get_engine(db_settings['DATABASE_URI']))


class GrantEntry(Base):
    __tablename__ = 'entries'
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    content = Column("content", String)
    link = Column("link", String(150))
    close_date = Column(DateTime)
    modified = Column(Boolean)
    etag = Column("etag", String(35))

    def __init__(self, title, content, link, close_date, etag, modified):
        self.title = title
        self.content = content
        self.link = link
        self.close_date = close_date
        self.modified = modified
        self.etag = etag

    @property
    def accepts_submission(self) -> bool:
        """
        accepts_submission returns true if the caller grant is still accepting
        submission in the current date
        :return: a boolean representing if submission are being accepted, true if yes
        """
        return self.close_date > datetime.utcnow()

    @property
    def is_modified(self) -> bool:
        """
        is_modified will return a bool value reprinting if the grant is a modified opportunity
        :return a boolean representing if the grant is modified, true if yes:
        """
        return self.modified

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id


if __name__ == '__main__':
    init_db()
