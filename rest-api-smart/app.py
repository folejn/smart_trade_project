from flask import Flask, jsonify, request

app = Flask(__name__)

client = app.test_client()

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
    return jsonify(shops)


@app.route('/shops', methods=['POST'])
def update_list():
    new_one = request.json
    shops.append(new_one)
    return jsonify(shops)


@app.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
    item = next((x for x in shops if x['id'] == shop_id), None)
    params = request.json
    if not item:
        return {'message': 'No shop with the same id'}, 400
    item.update(params)
    return item


@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    idx, _ = next((x for x in enumerate(shops) if x[1]['id'] == shop_id), (None, None))

    shops.pop(idx)
    return '', 204


if __name__ == '__main__':
    app.run()
