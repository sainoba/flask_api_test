import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db")
app.secret_key = "lfhasdlkjfhuiofydsonafusdiahfsdnlfsduinuiasdfh"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Store, "/store/<string:name>")  # http://127.0.0.1:5000/store/waltmart
api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/Carpet
api.add_resource(ItemsList, "/items")  # http://127.0.0.1:5000/items
api.add_resource(StoreList, "/stores")  # http://127.0.0.1:5000/stores
api.add_resource(UserRegister, "/register")  # http://127.0.0.1:5000/register

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
