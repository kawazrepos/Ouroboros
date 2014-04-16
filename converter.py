from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ouroboros.schemas.src.auth import User
from ouroboros.schemas.dst.personas import Persona
from ouroboros.converters.users import UserConverter

if __name__ == '__main__':

    src_engine = create_engine('sqlite:///kawaz.db')
    dst_engine = create_engine('sqlite:///db.sqlite3')
    Session = sessionmaker(bind=src_engine)
    ss = Session()
    ds = sessionmaker(bind=dst_engine)()

    for instance in ds.query(Persona):
        ds.delete(instance)
    ds.commit()

    for instance in ss.query(User):
        instance.__tablename__ = 'personas_persona'
        converter = UserConverter(instance, Persona)
        dst = converter.convert()
        ds.add(converter.convert())
    ds.commit()
