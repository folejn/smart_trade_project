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
