import hashlib

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    _password = Column(Text, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def _set_password(self, password):
        self._password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self._password == hashlib.sha1(password.encode('utf-8')).hexdigest()

    password = property(fset=_set_password)


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
