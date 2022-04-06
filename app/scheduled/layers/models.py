from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import psycopg2
from app.session_generator.create_session import get_engine, db_settings
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=get_engine(db_settings['DATABASE_URI']))


class GrantEntry(Base):
    __tablename__ = 'entries'
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    opp_num = Column("opp_num", String(50), unique=True)
    content = Column("content", String)
    link = Column("link", String(150))
    close_date = Column(DateTime)
    modified = Column(Boolean)
    etag = Column("etag", String(35))

    def __init__(self, title, content, link, close_date, etag, modified, opp_num):
        self.title = title
        self.opp_num = opp_num
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


class GrantEntrySchema(SQLAlchemySchema):
    class Meta:
        model = GrantEntry
        load_instance = True

    #id = auto_field()
    title = auto_field()
    #content = auto_field()
    link = auto_field()
    close_date = auto_field()
    modified = auto_field()
    #etag = auto_field()

if __name__ == '__main__':
    init_db()
