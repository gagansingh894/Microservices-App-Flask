from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask.json import JSONEncoder
from bson.json_util import default, dumps,loads
from bson.objectid import ObjectId
import requests

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        return default(obj)

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://gagan:password123456@cluster0.txmc2.mongodb.net/orderservice?retryWrites=true&w=majority"
app.json_encoder = CustomJSONEncoder
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def home():
    return 'This is orders microservice'

@app.route('/order', methods=['POST'])
def add_order():
    data = request.get_json()
    data['CustomerID'] = ObjectId(data['CustomerID'])
    data['BookID'] = ObjectId(data['BookID'])
    if list(data.keys()) == ['CustomerID', 'BookID', 'initialDate', 'deliveryDate']:
        mongo.db.orders.insert_one(data)
        return dumps(data)
    else:
        return jsonify({'message': 'Wrong Schema'})

@app.route('/orders', methods=['GET'])
def getall():
    orders = mongo.db.orders.find({})
    return dumps(orders)

@app.route('/order/<string:oid>', methods=['GET'])
def get_one(oid):
    data = loads(dumps(mongo.db.orders.find({'_id': ObjectId(oid)})))
    if len(data) != 0:
        res = requests.get("http://0.0.0.0:5001/customer/{}".format(str(data[0]['CustomerID']))).json()
        order_data = {"customerName": res[0]['name'], "bookTitle":''}
        res = requests.get("http://0.0.0.0:5000/book/{}".format(str(data[0]['BookID']))).json()
        order_data['bookTitle'] = res[0]['title']
        return dumps(order_data)
    else:
        return jsonify({'message': 'Invalid Request'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

