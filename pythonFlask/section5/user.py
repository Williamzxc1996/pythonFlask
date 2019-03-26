import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password
	#Noticed we didn't use self in this method, but use User
	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'SELECT * FROM users WHERE username=?'
		result = cursor.execute(query, (username,)) #the parameter has always to be in the form of tuple
		row = result.fetchone() #only return the first row, if no rows then return None
		if row:
			user = cls(*row) #cls(row[0], row[1], row[2]) they are in the correct order so could be replaced by *row
		else:
			user = None

		connection.close() #No need of commit(), we didn't change anything in the db
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'SELECT * FROM users WHERE id=?'
		result = cursor.execute(query, (_id,)) #the parameter has always to be in the form of tuple
		row = result.fetchone() #only return the first row, if no rows then return None
		if row:
			user = cls(*row) #cls(row[0], row[1], row[2]) they are in the correct order so could be replaced by *row
		else:
			user = None

		connection.close() #No need of commit(), we didn't change anything in the db
		return user 

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help='username cannot be left blank!')
	parser.add_argument('password', type=str, required=True, help='password cannot be left blank!')
	
	def post(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		data = UserRegister.parser.parse_args()
		#Because id is auto incremented, use NULL
		query = 'INSERT INTO users VALUES (NULL, ?, ?)'
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {'message': 'User created successfully.'}, 201
