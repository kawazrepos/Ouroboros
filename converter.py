from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ouroboros.schemas.src.blogs import Entry

if __name__ == '__main__':

    engine = create_engine('sqlite:///kawaz.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    for instance in session.query(Entry):
        print(instance.title)
        print(instance.body)
