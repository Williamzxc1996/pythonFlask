from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
			{
				'name': 'Nike',
				'items': [
					{
						'name': 'Air Max 90',
						'price': 199
					}
				]
			}
		 ]

#Get all the stores
@app.route('/stores',methods=['GET'])
def get_stores():
	return jsonify({'stores': stores})

#Create a new store
@app.route('/stores',methods=['POST'])
def create_store():
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)

#Get store by name
@app.route('/stores/<string:name>',methods=['GET'])
def get_store_byname(name):
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message': 'Store Not Found!'})

#Add new item to store
@app.route('/stores/<string:name>/items',methods=['POST'])
def add_item(name):
	request_data = request.get_json()
	new_item = {
		'name': request_data['name'],
		'price': request_data['price']
	}
	for store in stores:
		if store['name'] == name:
			store['items'].append(new_item)
			return jsonify(new_item)
	return jsonify({'message': 'Store Not Found!'})

app.run(port=5000)