from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #db will run on root directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jobie'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #create new end point -> /auth (sending usename and pw)
#auth return JWToken, then call identity function

api.add_resource(Store, '/store/<string:name>') #sub to decorator
api.add_resource(Item, '/item/<string:name>') #sub to decorator
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=4998, debug=True)
