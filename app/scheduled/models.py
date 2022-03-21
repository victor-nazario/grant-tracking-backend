from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, event
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True,
                       **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    Model.metadata.create_all(bind=engine)


class GrantEntry(Model, search.Indexable):
    __tablename__ = 'entries'
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(75))
    content = Column("content", String)
    link = Column("link", String(150), unique=True)
    close_date = Column(Datetime)
    modified = Column(Boolean)
    etag = Column("etag", String(35))

    def __init__(self, title, content, link, close_date, etag):
        self.title = title
        self.content = content
        self.link = link
        self.close_date = close_date
        self.etag = etag

    @property
    def accepts_submission(self):
        return self.close_date > datetime.utcnow()

    @property
    def is_modified(self):
        return self.modified

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id
