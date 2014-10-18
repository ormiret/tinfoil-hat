from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from config import DB_CONN

Base = declarative_base()

class Body(Base):
    __tablename__ = 'body'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    url = Column(String(1000))

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer(), primary_key=True)
    body = Column(Integer(), ForeignKey('body.id'))
    body_req_id = Column(String(20))
    submission_date = Column(DateTime())
    response_date = Column(DateTime())
    title = Column(String(200))
    type = Column(String(10)) 

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer(), primary_key=True)
    url = Column(String(1000))
    request = Column(Integer(), ForeignKey('request.id'))
    text = Column(Text())

class RequestTag(Base):
    __tablename__ = 'request_tag'
    id = Column(Integer(), primary_key=True)
    request = Column(Integer(), ForeignKey('request.id'))
    tag = Column(String(20))

def setup_db():
    engine = create_engine(DB_CONN)
    Base.metadata.create_all(engine)
    

def get_session():
    engine = create_engine(DB_CONN)
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    return DBSession()
