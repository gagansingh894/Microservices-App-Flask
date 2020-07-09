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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
