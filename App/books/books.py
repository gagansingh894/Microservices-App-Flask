from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from bson.json_util import dumps, default
from bson.objectid import ObjectId

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): 
        return default(obj)


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://gagan:password123456@cluster0.txmc2.mongodb.net/bookservice?retryWrites=true&w=majority"
app.json_encoder = CustomJSONEncoder
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def home():
    return "This is our books entry point"

@app.route('/book', methods=['POST'])
def insert():
    data = request.get_json()
    if list(data.keys()) == ['title', 'author', 'numOfPages', 'publisher']:
        result = mongo.db.books.insert_one(data)
        return dumps(data)
    else:
        return jsonify({'message': 'Wrong Schema!'})

@app.route('/books', methods=['GET'])
def getall():
    books = mongo.db.books.find({})
    return dumps(books)

@app.errorhandler(404)
@app.route('/book/<string:bid>', methods=['GET', 'DELETE'])
def getone(bid):
    if request.method == 'GET':
        try:
            data = request.get_json()
            book = mongo.db.books.find({'_id': ObjectId(bid)})
            return dumps(book)
        except:
            return jsonify({'message': '404 error'})
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            mongo.db.books.delete_one({'_id': ObjectId(bid)})
            return jsonify({'message': 'Record deleted'})
        except:
            return jsonify({'message': '404 error'})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': '404 error'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)