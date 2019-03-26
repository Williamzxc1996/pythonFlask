from flask import Flask, request
#No need to do jsonify when talking to flask_restful
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
#For authentication
app.secret_key = 'jose'
api = Api(app)
#JWT create a new endpoint '/auth', it takes username and password as input
#and send them to authenticate method
#Then the endpoint return a JWT token, then we send along the JWT token
#with every request we make, which calls identity method
jwt = JWT(app, authenticate, identity)
#Use in-memory database which is a python list
items = []

#Define item class extend Resource
class Item(Resouce):
	#parse the payload in the request, have many parameters in the add_argument function
	#Now the parse is belong to the Item class
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

	#jwt_requied is decorator, it means that we need to authenticate before get is called
	@jwt_required()
	def get(self, name):
		#next() gives the next item in the filter object, if next() doesn't find an item return None
		item = next(filter(lambda x: x['name'] == name, items), None)
		#If item is None return 404, else return 200
		return {'item': item}, 200 if item else 404

	#No need to jsonify
	def post(self, name):
		#If the item name already exists, bad request return 400
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': 'An item with name {} already exists'.format(name)}, 400

		request_data = Item.parser.parse_args()

		item = {
			'name': name,
			'price': request_data['price']
		}
		items.append(item)
		#successfully created, status code is 201 
		return item, 201

	def delete(self, name):
		#We need global here, because when we are assigning, there are
		#two possibilities, in python by default, it'll assume you are
		#creating a local variable named items
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}

	def put(self, name):
		request_data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {
				'name': name,
				'price': request_data['price']
			}
		else:
			item.update(request_data)
		return item


class ItemList(Resource):
	def get(self):
		return {
			'items': items
		}

#Associate the endpoint with our api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
#Set debug=True to show the detailed error message
app.run(port=5000, debug=True)