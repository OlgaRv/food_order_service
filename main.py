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


def create_db_and_table():
    # Создаём базу данных
    conn = sqlite3.connect('zero_order_service.db')
    cursor = conn.cursor()

    # Создаем таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category_dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
    ''')

    # Закрываем соединение с базой данных
    conn.commit()
    conn.close()

def add_category(category_name):
    # Подключаемся к базе данных
    conn = sqlite3.connect('zero_order_service.db')
    cursor = conn.cursor()

    # Добавляем новую категорию
    cursor.execute('INSERT INTO Category_dishes (category_name) VALUES (?)', (category_name,))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


def create_table_status():
    conn = sqlite3.connect("zero_order_service.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)""")

    conn.commit()
    conn.close()

def add_order_status(name):
    conn = sqlite3.connect("zero_order_service.db")
    cur = conn.cursor()
    cur.execute("insert into create_table_status(name), value(?,)", (name))
    conn.commit()
    conn.close()

# Пример использования функций
create_db_and_table()  # Создаем базу данных и таблицу
create_table_status()
add_category('Супы')  # Добавляем категорию 'Супы'
add_category('Гарниры')  # Добавляем категорию 'Гарниры'
add_order_status("Новый")
add_order_status("В работе")
add_order_status("На доставку")
add_order_status("Доставлен")
add_order_status("Оплачен")


def create_table_orders():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    sum FLOAT CHECK (Sum >= 0),
    status_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(status_id) REFERENCES Order_status(id))
    ''')

    conn.commit()
    conn.close()

# Вызываем функцию
create_table_orders()



