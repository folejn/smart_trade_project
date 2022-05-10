from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "af6b72e8e3cc4dd1a1f40a9e0b029ad6"

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

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
@jwt_required()
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
@jwt_required()
def get_products():
    products = Product.query.all()
    serialised = []
    for product in products:
        serialised.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
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


'''@app.route('/users', methods=['GET'])
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
    return jsonify(serialised)'''


@app.route('/shops', methods=['POST'])
@jwt_required()
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
@jwt_required()
def new_product():
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


'''@app.route('/users', methods=['POST'])
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
    return jsonify(serialised)'''


@app.route('/transaction', methods=['POST'])
def new_transaction():
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
@jwt_required()
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
@jwt_required()
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

@app.route('/products/name/<string:product_subname>', methods=['GET'])
@jwt_required()
def search_product_by_name(product_subname):
    products = Product.query.filter(Product.name.contains(product_subname)).all()
    if not products:
        return jsonify([])
    serialised = []
    for product in products:
        serialised.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price
        })
    return jsonify(serialised)

@app.route('/products/description/<string:product_subdescr>', methods=['GET'])
@jwt_required()
def search_product_by_desc(product_subdescr):
    products = Product.query.filter(Product.description.contains(product_subdescr)).all()
    if not products:
        return jsonify([])
    serialised = []
    for product in products:
        serialised.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price
        })
    return jsonify(serialised)


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
@jwt_required()
def delete_shop(shop_id):
    item = Store.query.filter(Store.id == shop_id).first()
    if not item:
        return {'message': 'No shop with the same id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods={'POST'})
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


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
