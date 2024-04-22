import sqlite3
conn = sqlite3.connect('Users.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS User_role
(id INTEGER PRIMARY KEY,
name STRING UNIQUE)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
phone STRING,
address STRING,
sum_of_orders FLOAT,
discount FLOAT,
user_role STRING,
FOREIGN KEY(user_role) REFERENCES User_role(name))
''')

conn.commit()
conn.close()
