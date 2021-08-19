from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    #to limit the value to parse
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "The store with name '{}' already exists".format(name)}, 400 #400 bad request

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message', 'An error occured while creating the store'}, 500 #internal server error

        return store.json(), 201 #201 for created, 202 is when there's a delay


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
