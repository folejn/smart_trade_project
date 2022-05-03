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


@app.route('/shops', methods=['GET'])
def get_list():
    stores = Store.query.all()
    serialised = []
    for store in stores:
        serialised.append({
            'id': store.id,
            'title': store.title,
            'description': store.description
        })
    return jsonify(serialised)


@app.route('/shops', methods=['POST'])
def update_list():
    new_one = Store(**request.json)
    session.add(new_one)
    session.commit()
    serialised = {
        'id': new_one.id,
        'title': new_one.title,
        'description': new_one.description
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


@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    item = Store.query.filter(Store.id == shop_id).first()
    if not item:
        return {'message': 'No shop with the same id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()



if __name__ == '__main__':
    app.run()
