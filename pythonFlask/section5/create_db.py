import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
#In python its a tuple, the thing we retreive back is also a list of tuples
#Auto incremented id use INTEGER PRIMARY KEY 
query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text UNIQUE, password text)"
cursor.execute(query)

# users = [(1, 'Jose', 'asdf'),
# 		 (2, 'Billy', 'qwer'),
# 		 (3, 'Zhou', 'zxcv')]
# query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.executemany(query,users) #Way to insert multiple users into db

connection.commit() #actually save all the changes into the disc
connection.close()