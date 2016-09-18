from sqlalchemy import *
from sqlalchemy.orm import *
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(String(255))
    active = db.Column(Boolean())
    role = db.Column(String(40))

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


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(Integer, primary_key=True)
    client = db.Column(String(50))

    def __init__(self, client=None):
        self.client = client

    def __repr__(self):
        return "<Client(id='%d', client='%s'>" % (self.id, self.client)


class ProductArea(db.Model):
    __tablename__ = 'productarea'
    id = db.Column(Integer, primary_key=True)
    productarea = db.Column(String(50))

    def __init__(self, productarea=None):
        self.productarea = productarea

    def __repr__(self):
        return '<id %d, productarea %s>' % (self.id, self.productarea)


class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(50))
    description = db.Column(String(9000))
    client_id = db.Column(Integer, ForeignKey('client.id'), nullable=False)
    clientPriority = db.Column(Integer)
    targetDate = db.Column(DateTime)
    url = db.Column(String(100))
    productArea = db.Column(Integer, ForeignKey('productarea.id'), nullable=False)
    active = db.Column(Integer, nullable=False)
    assigned = db.Column(String(50), ForeignKey('users.name'), nullable=False)
    completed = db.Column(Integer, ForeignKey('status.id'), default=1)

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

class FeatureStatus(db.Model):
    __tablename__ = 'status'
    id = db.Column(Integer, primary_key=True)
    status = db.Column(String(10))

    def __repr__(self):
        return self.status

class MessageBoard(db.Model):
    __tablename__ = 'messageboard'
    id = db.Column(Integer, primary_key=True)
    date = db.Column(DateTime, nullable=False)
    message = db.Column(String(4000))
    username = db.Column(String(50))
    feature_id = db.Column(Integer, ForeignKey('feature.id'))
    feature = relationship("Feature", foreign_keys='MessageBoard.feature_id')

    def __init__(self, message=None, username=None, feature_id=None, date=None):
        self.message = message
        self.username = username
        self.feature_id = feature_id
        self.date = date

    def __repr__(self):
        return self.message