from datetime import datetime

from flask import Flask
from flask_sqlalchemy import Model
from pip._internal.commands import search
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, event, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation

app = Flask(__name__)
app.config['DATABASE_URI'] = ''
app.config['DATABASE_CONNECT_OPTIONS'] = ''
engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True,
                       **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

metadata = MetaData()


def init_db():
    metadata.create_all(bind=engine)


class GrantEntry(Model):
    __tablename__ = 'entries'
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(75))
    content = Column("content", String)
    link = Column("link", String(150), unique=True)
    close_date = Column(datetime)
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
    def accepts_submission(self):
        return self.close_date > datetime.utcnow()

    @property
    def is_modified(self):
        return self.modified

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id


if __name__ == '__main__':
    app.run()
