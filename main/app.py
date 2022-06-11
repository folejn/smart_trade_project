from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import datetime


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "af6b72e8e3cc4dd1a1f40a9e0b029ad6"

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from main.models import *

Base.metadata.create_all(bind=engine)


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
            'quantity': product.quantity,
            'seller_address': product.owner.address
        })
    return jsonify(serialised)


@app.route('/transaction', methods=['GET'])
def get_transaction():
    transactions = Transaction.query.all()
    serialised = []
    for transaction in transactions:
        if transaction.sides is not None:
            addresses = [side.address for side in transaction.sides]
            serialised.append({
                'id': transaction.id,
                'date': transaction.date,
                'price': transaction.price,
                'seller_address': addresses[0],
                'buyer_address': addresses[1]
            })
        else:
            serialised.append({
                'id': transaction.id,
                'date': transaction.date,
                'price': transaction.price
            })
    return jsonify(serialised)
'''
@app.route('/user/<int: user_id>/transaction', methods=['GET'])
def get_users_transaction(id):
    transactions = Transaction.query.all()
    serialised = []
    for transaction in transactions:
        if transaction.sides is not None:
            addresses = [side.address for side in transaction.sides]
            serialised.append({
                'id': transaction.id,
                'date': transaction.date,
                'price': transaction.price,
                'seller_address': addresses[0],
                'buyer_address': addresses[1]
            })
        else:
            serialised.append({
                'id': transaction.id,
                'date': transaction.date,
                'price': transaction.price
            })
    return jsonify(serialised)
'''

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

@app.route('/products/buy', methods=['POST'])
@jwt_required
def buy_product():
    products = request.json
    pass

@app.route('/products', methods=['POST'])
@jwt_required()
def new_product():
    new_one = Product(**request.json)
    user_id = get_jwt_identity()
    new_one.users_id = user_id
    session.add(new_one)
    session.commit()
    return 'New product added!', 200


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
@jwt_required()
def new_transaction():
    price = request.json['price']
    date = datetime.datetime.now()
    new_one = Transaction(date = date, price=price)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'price': new_one.price,
        'date': new_one.date
    }
    return jsonify(serialised),200


@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    item = Product.query.filter(Product.id == product_id).first()
    params = request.json
    if not item:
        return {'message': 'No product with the same id'}, 400
    owner = item.owner
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialised = {
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'status': item.status,
        'quantity': item.quantity,
        'seller_address': owner.address
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
        'price': item.price
    }
    return serialised


@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    if User.query.filter(User.email == email).first():
        return {'message': 'Email is already exist.'}, 400
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods={'POST'})
def login():
    email = request.json['email']
    if not User.query.filter(User.email == email).first():
        return {'message': 'Email does not exist.'}, 400
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
    session.commit()
    return '', 204


@app.route('/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    item = Transaction.query.filter(Transaction.id == transaction_id).first()
    if not item:
        return {'message': 'No transaction with the same id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()


