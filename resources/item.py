from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemsList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True,
        help="This can't be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        response = item.json() if item else (
            {"message": "item not found"}, 404)
        return response

    def post(self, name):
        response = {"message": f"An item called '{name}' already exists"}, 400
        item = ItemModel.find_by_name(name)
        if item is None:
            data = self.parser.parse_args()
            item = ItemModel(name, **data)
            try:
                item.save_to_db()
                response = item.json(), 201
            except:
                response = {"message": "There was an error"}, 500  # Internal server error
        return response

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item
