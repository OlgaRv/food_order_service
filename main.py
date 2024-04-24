import sqlite3


def create_db_and_table():
    try:
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User_role (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        conn.close()

def add_user(name, role=None):
    # Если роль не указана, автоматически присваиваем роль "клиент"
    if role is None:
        role = 'клиент'

    try:
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO User_role (name, role) VALUES (?, ?)', (name, role))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()

def update_user_role(name, new_role):
    try:
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE User_role SET role = ? WHERE name = ?', (new_role, name))
        if cursor.rowcount == 0:
            print("Пользователь не найден.")
        else:
            print("Роль успешно обновлена.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении роли пользователя: {e}")
    finally:
        conn.close()


def create_table_orders():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY,
    sum FLOAT CHECK (Sum >= 0),
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(status_id) REFERENCES Order_status(id))
    ''')

    conn.commit()
    conn.close()

def create_table_dishes():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS dishes
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER CHECK (price >= 0),
    image TEXT,
    FOREIGN KEY(category_id) REFERENCES Category(id))
    ''')

    conn.commit()
    conn.close()

def create_table_users():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('''    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone STRING,    address STRING,
    sum_of_orders FLOAT,    discount FLOAT,
    user_role INTEGER,
    FOREIGN KEY(user_role) REFERENCES User_role(id))
    ''')
    conn.commit()
    conn.close()

    def create_table_category():
        # Создаём базу данных
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()
        # Создаем таблицу
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL)
        ''')
        # Закрываем соединение с базой данных
        conn.commit()
        conn.close()
