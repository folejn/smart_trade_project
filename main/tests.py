from app import client
from models import *


def test_get():
    res = client.get('/shops')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Store.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        #       'id': 4,
        'title': 'SwissTime',
        'description': 'One second.'
    }

    res = client.post('/shops', json=data)

    assert res.status_code == 200

    assert res.get_json()['title'] == data['title']


def test_put():
    res = client.put('/shops/1', json={'name': 'UPD'})

    assert res.status_code == 200
    assert Store.query.get(1).name == 'UPD'


def test_delete():
    res = client.delete('/shops/1')

    assert res.status_code == 204
    assert Store.query.get(1) is None


def test_get_product():
    res = client.get('/products')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Product.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post_product():
    data = {
        'name': 'prod1',
        'status': 'created',
        'price': 10,
        'quantity': 3
    }

    res = client.post('/products', json=data)

    assert res.status_code == 200

    assert res.get_json()['name'] == data['name']


def test_put_product():
    res = client.put('/products/1', json={'name': 'prod1'})

    assert res.status_code == 200
    assert Product.query.get(1).name == 'prod1'


def test_delete_product():
    res = client.delete('/products/1')

    assert res.status_code == 204
    assert Product.query.get(1) is None


def test_get_transaction():
    res = client.get('/transaction')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Transaction.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post_transaction():
    data = {
        #       'id': 4,
        'date': 5360,
        'quantity': 5
    }

    res = client.post('/transaction', json=data)

    assert res.status_code == 200

    assert res.get_json()['title'] == data['title']


def test_put_transaction():
    res = client.put('/transaction/1', json={'name': 'UPD'})

    assert res.status_code == 200
    assert Transaction.query.get(1).name == 'UPD'


def test_delete_transaction():
    res = client.delete('/transaction/1')

    assert res.status_code == 204
    assert Transaction.query.get(1) is None
