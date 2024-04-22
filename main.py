import sqlite3

def create_table_users():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone STRING,
    address STRING,
    sum_of_orders FLOAT,
    discount FLOAT,
    user_role INTEGER,
    FOREIGN KEY(user_role) REFERENCES User_role(id))
    ''')

    conn.commit()
    conn.close()

# Вызываем функцию
create_table_users()

