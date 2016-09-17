from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    role = Column(String(40))

    def __init__(self, name=None, email=None, password=None, active=None, confirmed_at=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.confirmed_at = confirmed_at
        self.role = role

    def __repr__(self):
        return "<User(id='%d', name='%s', email='%s', password='%d', active='%d', confirmed_at='%s', role='%s'>" % (
        self.id, self.name, self.email, self.password, self.active, self.confirmed_at, self.role)


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    client = Column(String(50))

    def __init__(self, client=None):
        self.client = client

    def __repr__(self):
        return "<Client(id='%d', client='%s'>" % (self.id, self.client)


class ProductArea(Base):
    __tablename__ = 'productarea'
    id = Column(Integer, primary_key=True)
    productarea = Column(String(50))

    def __init__(self, productarea=None):
        self.productarea = productarea

    def __repr__(self):
        return '<id %d, productarea %s>' % (self.id, self.productarea)


class Feature(Base):
    __tablename__ = 'feature'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(200))
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    clientPriority = Column(Integer)
    targetDate = Column(DateTime)
    url = Column(String(100))
    productArea = Column(Integer, ForeignKey('productarea.id'), nullable=False)
    active = Column(Integer, nullable=False)
    assigned = Column(Integer, ForeignKey('users.name'), nullable=False)
    completed = Column(Integer, ForeignKey('status.id'), default=1)

    client = relationship('Client', foreign_keys='Feature.client_id')
    product = relationship('ProductArea', foreign_keys='Feature.productArea')
    userassigned = relationship('User', foreign_keys='Feature.assigned')
    status = relationship('FeatureStatus', foreign_keys='Feature.completed')

    def __init__(self, title=None, description=None, client_id=None, clientPriority=None, targetDate=None, url=None,
                 productArea=None, active=None, assigned=None, completed=None):
        self.title = title
        self.description = description
        self.client_id = client_id
        self.clientPriority = clientPriority
        self.targetDate = targetDate
        self.url = url
        self.productArea = productArea
        self.active = active
        self.assigned = assigned
        self.completed = completed

    def __repr__(self):
        return "<Feature(id='%d', title='%s', description='%s', clientid='%d', clientname='%s', clientPriority='%d', url='%s', productArea_id='%d', productarea='%s', userassigned='%s', active='%d') >" % (
            self.id, self.title, self.description, self.client_id, self.client.client, self.clientPriority,
            self.targetDate,
            self.url, self.productArea, self.product.productarea, self.userassigned,
             self.active)

class FeatureStatus(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    status = Column(String(10))

    def __repr__(self):
        return self.status

class MessageBoard(Base):
    __tablename__ = 'messageboard'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    message = Column(String(2000))
    username = Column(String(50))
    feature_id = Column(Integer, ForeignKey('feature.id'))
    feature = relationship("Feature", foreign_keys='MessageBoard.feature_id')

    def __init__(self, message=None, username=None, feature_id=None, date=None):
        self.message = message
        self.username = username
        self.feature_id = feature_id
        self.date = date

    def __repr__(self):
        return self.message