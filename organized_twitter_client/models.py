import hashlib

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    )

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    query = DBSession.query_property()
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    _password = Column(Text, nullable=False)
    group = ['USERS']

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def _set_password(self, password):
        self._password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self._password == hashlib.sha1(password.encode('utf-8')).hexdigest()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def add_user(cls, name, password):
        user = User(name, password)
        DBSession.add(user)

    password = property(fset=_set_password)


class RootFactory(object):
    __acl__ = [(Allow, 'USERS', 'view')]

    def __init__(self, request):
        pass