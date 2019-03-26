from user import User
from werkzeug.security import safe_str_cmp

# #In-memory database for registered user
# users = [
# 	User(1, 'Bob', 'asdf')
# ]

# #Set comprehension
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
	#user = username_mapping.get(username, None)
	user = User.find_by_username(username)
	print(user.username)
	print(user.password)
	if user and user.password == password:
		return user

def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)