from main.app import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt

transaction_user = db.Table('junction', Base.metadata,
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'))
)

transaction_product = db.Table('junction_2', Base.metadata,
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('products_id', db.Integer, db.ForeignKey('products.id'))
)
class Store(Base):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    surname = db.Column(db.String(30), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    products = relationship('Product', backref='owner', lazy=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(30), nullable=True)
    #shops = relationship('Store', backref='user', lazy=True)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))


    def get_token(self, expire_time=240):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token


    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

class Product(Base):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Transaction(Base):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    sides = relationship("User",
                    secondary=transaction_user, backref='transactions')
    wares = relationship("Product",
                    secondary=transaction_product, backref='transactions')
