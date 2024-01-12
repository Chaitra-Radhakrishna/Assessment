#pip install flask
#pip install Flask Flask-HTTPAuth

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# In-memory user and product database (replace with a real database in production)
users = {}
products = []

@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username in users:
        return jsonify({'error': 'Username already exists'}), 400

    users[username] = password
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/products', methods=['GET'])
@auth.login_required
def get_products():
    return jsonify({'products': products})

@app.route('/products', methods=['POST'])
@auth.login_required
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or not price:
        return jsonify({'error': 'Name and price are required'}), 400

    product = {'id': len(products) + 1, 'name': name, 'price': price}
    products.append(product)
    return jsonify({'message': 'Product added successfully', 'product': product}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
@auth.login_required
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify({'product': product})
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
