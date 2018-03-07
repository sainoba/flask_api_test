from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        response = {"message": "Store not found"}, 404
        if store:
            response = store.json()
        return response

    def post(self, name):
        store = StoreModel.find_by_name(name)
        response = ""
        if store is None:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                response = {"message": "Error saving the store"}, 500
            else:
                response = store.json()
        else:
            response = {"message": f"Store '{name}' already exists"}, 400
        return response

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        response = {"message": f"Store '{name}' deleted"}
        return response



class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
