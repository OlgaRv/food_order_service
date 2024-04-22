import sqlite3
conn = sqlite3.connect('Users.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
phone STRING,
address STRING,
sum_of_orders FLOAT,
discount FLOAT)
''')

conn.commit()
conn.close()
