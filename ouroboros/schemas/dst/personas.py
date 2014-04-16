from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Persona(Base):
    __tablename__ = 'personas_persona'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    last_login = Column(DateTime)
    date_joined = Column(DateTime)
    nickname = Column(String)
    quotes = Column(String)
    avatar = Column(String)
    gender = Column(String)
