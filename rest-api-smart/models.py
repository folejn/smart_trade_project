from app import db, session, Base
from sqlalchemy.orm import relationship

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
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    products = relationship('Product', backref='owner', lazy=True)


class Product(Base):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)


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
