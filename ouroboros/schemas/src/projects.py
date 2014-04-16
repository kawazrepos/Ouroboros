from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects_project'

    id = Column(Integer, primary_key=True)
    pub_state = Column(Integer)
    status = Column(String)
    title = Column(String)
    slug = Column(String)
    body = Column(String)
    body_markup_type = Column(String)
    icon = Column(String)
    category_id = Column(Integer)
    _body_rendered = Column(String)
    author_id = Column(Integer)
    group_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Category(Base):
    __tablename__ = 'projects_category'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    parent_id = Column(Integer)

class ProjectRelation(Base):
    __tablename__ = 'projects_project_members'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
