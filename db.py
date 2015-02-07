from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from config import DB_CONN

from datetime import datetime, date

Base = declarative_base()

class AutoSerialize(object):
    'Mixin for retrieving public fields of model in json-compatible format'
    __public__ = None

    def get_public(self, exclude=(), extra=()):
        "Returns model's PUBLIC data for jsonify"
        data = {}
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        for k, field in  keys:
            if public and k not in public: continue
            if k in exclude: continue
            value = self._serialize(field.value)
            if value:
                data[k] = value
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if type(value) in (datetime, date):
            ret = value.isoformat()
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AutoSerialize in value.__class__.__bases__:
            ret = value.get_public()
        else:
            ret = value

        return ret

class Body(Base):
    __tablename__ = 'body'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    url = Column(String(1000))

class Request(Base, AutoSerialize):
    __tablename__ = 'request'
    __public__ = ('id', 'body', 'body_req_id', 'submission_date', 'response_date', 'title', 'type')
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
    engine = create_engine(DB_CONN, encoding='utf-8')
    Base.metadata.create_all(engine)
    

def get_session():
    engine = create_engine(DB_CONN, encoding='utf-8')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    return DBSession()
