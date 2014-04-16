from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'blogs_entry'

    id = Column(Integer, primary_key=True)
    pub_state = Column(String)
    title = Column(String)
    body = Column(String)
    body_markup_type = Column(String)
    category_id = Column(Integer)
    _body_rendered = Column(String)
    author_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    publish_at = Column(DateTime)
    publish_at_date = Column(Date)

class Category(Base):
    __tablename__ = 'blogs_category'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    author_id = Column(Integer)