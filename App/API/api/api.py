from flask import Flask, redirect
from flask.json import jsonify

app = Flask(__name__)

BOOKROUTE = 'http://0.0.0.0:5001'
CUSTOMERSROUTE = 'http://0.0.0.0:5002'
ORDERSROUTE = 'http://0.0.0.0:5003'

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API Gateway'})

@app.route('/api/books', methods=['GET'])
def books_route():
    return redirect(BOOKROUTE) 

@app.route('/api/customers', methods=['GET'])
def customers_route():
    return redirect(CUSTOMERSROUTE)

@app.route('/api/orders', methods=['GET'])
def orderss_route():
    return redirect(ORDERSROUTE)

@app.errorhandler(404)
def no_route(e):
    return jsonify({'message': '404 Error'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
