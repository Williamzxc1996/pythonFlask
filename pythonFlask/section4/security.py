from user import User

#In-memory database for registered user
users = [
	User(1, 'Bob', 'asdf')
]

#Set comprehension
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
	#dic.get() is another way to access the dictionary, the advantage is that
	#you can set a default value like get(username, None)
	user = username_mapping.get(username, None)
	if user and user.password == password:
		return user
#payload is Flask-JWT message, it contains user_id, it helps to
#determine if the user is already logged in
def identity(payload):
	user_id = payload['identity']
	return userid_mapping.get(user_id, None)