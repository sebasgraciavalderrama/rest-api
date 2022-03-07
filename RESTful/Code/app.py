from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT
from flask_jwt_extended import jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'myappsecret'
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    #@jwt_required() - CHECK THIS
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with that name '{}' already exists.".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item:
            items.remove(item)
            return {"message": "Item deleted"}, 202
        return {"message": "Item not found"}, 400

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)