from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

shops = [
    {
        'id': 1,
        'title': 'AliExpress',
        'description': 'More than everything.'
    },
    {
        'id': 2,
        'title': 'Allegro',
        'description': 'Today and right now.'
    },
    {
        'id': 3,
        'title': 'Random shop',
        'description': 'Random description.'
    }
]

products = [
    {
        'id': 1,
        'name': 'prod1',
        'price': 10,
        'status': 'created',
        'quantity': 3
    },
    {
        'id': 2,
        'name': 'prod2',
        'price': 10,
        'status': 'approved',
        'quantity': 2
    },
    {
        'id': 3,
        'name': 'prod3',
        'price': 5,
        'status': 'created',
        'quantity': 7
    }
]

transaction = [
    {
        'id': 1,
        'date': 5613,
        'quantity': 10,
        'price': 25
    },
    {
        'id': 2,
        'date': 6113,
        'quantity': 10,
        'price': 24
    }
]


@app.route('/shops', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    serialised = []
    for store in stores:
        serialised.append({
            'id': store.id,
            'title': store.title,
            'description': store.description
        })
    return jsonify(serialised)


@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    serialised = []
    for product in products:
        serialised.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'status': product.status,
            'quantity': product.quantity
        })
    return jsonify(serialised)


@app.route('/transaction', methods=['GET'])
def get_transaction():
    transactions = Transaction.query.all()
    serialised = []
    for transaction in transactions:
        serialised.append({
            'id': transaction.id,
            'date': transaction.date,
            'quantity': transaction.quantity,
            'price': transaction.price
        })
    return jsonify(serialised)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialised = []
    for user in users:
        serialised.append({
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birth date': user.birth_date
        })
    return jsonify(serialised)


@app.route('/shops', methods=['POST'])
def update_stores():
    new_one = Store(**request.json)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'title': new_one.title,
        'description': new_one.description
    }
    return jsonify(serialised)


@app.route('/products', methods=['POST'])
def update_products():
    new_one = Product(**request.json)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'name': new_one.name,
        'price': new_one.price,
        'status': new_one.status,
        'quantity': new_one.quantity
    }
    return jsonify(serialised)


@app.route('/users', methods=['POST'])
def update_users():
    new_one = Store(**request.json)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'name': new_one.name,
        'surname': new_one.surname,
        'birth date': new_one.birth_date
    }
    return jsonify(serialised)


@app.route('/transaction', methods=['POST'])
def update_transaction():
    new_one = Transaction(**request.json)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'date': new_one.date,
        'quantity': new_one.quantity,
        'price': new_one.price
    }
    return jsonify(serialised)


@app.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
    item = Store.query.filter(Store.id == shop_id).first()
    params = request.json
    if not item:
        return {'message': 'No shop with the same id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'title': item.title,
        'description': item.description
    }
    return serialised


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    item = Product.query.filter(Product.id == product_id).first()
    params = request.json
    if not item:
        return {'message': 'No product with the same id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'status': item.status,
        'quantity': item.quantity
    }
    return serialised


@app.route('/transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    item = Transaction.query.filter(Transaction.id == transaction_id).first()
    params = request.json
    if not item:
        return {'message': 'No transaction with the same id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'date': item.date,
        'quantity': item.quantity,
        'price': item.price
    }
    return serialised


@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    item = Store.query.filter(Store.id == shop_id).first()
    if not item:
        return {'message': 'No shop with the same id'}, 400
    session.delete(item)
    session.commite()
    return '', 204


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    item = Product.query.filter(Product.id == product_id).first()
    if not item:
        return {'message': 'No product with the same id'}, 400
    session.delete(item)
    session.commite()
    return '', 204


@app.route('/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    item = Transaction.query.filter(Transaction.id == transaction_id).first()
    if not item:
        return {'message': 'No transaction with the same id'}, 400
    session.delete(item)
    session.commite()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()



if __name__ == '__main__':
    app.run()