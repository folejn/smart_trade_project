from app import client

def test_get():
    res = client.get('/shops')

    assert res.status_code == 200

    assert len(res.get_json()) == 3
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'id': 4,
        'title': 'SwissTime',
        'description': 'One second.'
    }

    res = client.post('/shops', json=data)

    assert res.status_code == 200

    assert len(res.get_json()) == 4
    assert res.get_json()[-1]['title'] == data['title']
