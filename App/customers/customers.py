from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from bson.json_util import dumps, default
from bson.objectid import ObjectId

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        return default(obj)


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://gagan:password123456@cluster0.txmc2.mongodb.net/customerservice?retryWrites=true&w=majority"
app.json_encoder = CustomJSONEncoder
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def hello():
    return "This is customer microservice"

@app.route('/customer', methods=['POST'])
def addcustomer():
    data = request.get_json()
    if list(data.keys()) == ['name', 'age', 'address']:
        result = mongo.db.customers.insert_one(data)
        return dumps(data)
    else:
        return jsonify({'message': 'Wrong Schema'})

@app.route('/customers', methods=['GET'])
def getall():
    customers = mongo.db.customers.find()
    return dumps(customers)

@app.errorhandler(404)
@app.route('/customer/<string:cid>', methods=['GET', 'DELETE'])
def getone(cid):
    if request.method == 'GET':
        try:
            data = request.get_json()
            result = mongo.db.customers.find({'_id': ObjectId(cid)})
            return dumps(result)
        except:
            return jsonify({'message': '404 not found'})
    elif request.method == 'DELETE':
        try:
            mongo.db.customers.delete_one({'_id': ObjectId(cid)})
            return jsonify({'message': 'record deleted'})
        except:
            return jsonify({'message': '404 not found'})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'message': '404 not found'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)