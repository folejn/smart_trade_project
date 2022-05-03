from app import db, session, Base


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


class Product(Base):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


class Transaction(Base):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)
