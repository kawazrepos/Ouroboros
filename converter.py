from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker
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

if __name__ == '__main__':

    engine = create_engine('sqlite:///kawaz.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    for instance in session.query(Entry):
        print(instance.title)
        print(instance.body)
