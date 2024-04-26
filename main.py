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

        cursor.execute('INSERT INTO Users (name, user_role) VALUES (?, ?)', (name, role))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    #finally:



def update_user_role(name, new_role):
    try:
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET role = ? WHERE name = ?', (new_role, name))
        if cursor.rowcount == 0:
            print("Пользователь не найден.")
        else:
            print("Роль успешно обновлена.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении роли пользователя: {e}")
    finally:
        conn.close()


# def create_table_orders():
#     conn = sqlite3.connect('zero_order_service.db')
#     cur = conn.cursor()
#
#     cur.execute('''
#     CREATE TABLE IF NOT EXISTS orders
#     (id INTEGER PRIMARY KEY  AUTOINCREMENT,
#     sum FLOAT CHECK (Sum >= 0),
#     FOREIGN KEY(user_id) REFERENCES Users(id),
#     FOREIGN KEY(status_id) REFERENCES Order_status(id))
#     ''')
#
#     conn.commit()
#     conn.close()

def create_table_dishes():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS dishes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER CHECK (price >= 0),
    image TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES Category_dishes(id))
    ''')

    conn.commit()
    conn.close()

def create_table_users():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        sum_of_orders FLOAT,
        discount FLOAT,
        user_role INTEGER,
        FOREIGN KEY(user_role) REFERENCES User_role(id)
    )
    ''')
    conn.commit()
    conn.close()

def create_table_category():
    # Создаём базу данных
    conn = sqlite3.connect('zero_order_service.db')
    cursor = conn.cursor()
    # Создаем таблицу
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Category_dishes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL)
            ''')
    # Закрываем соединение с базой данных
    conn.commit()
    conn.close()

def add_category(category_name):    # Подключаемся к базе данных
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
    cur.execute('''CREATE TABLE IF NOT EXISTS order_status
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def add_order_status():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute("Select * From order_status where name=?",('Новый',))
    check1 = cur.fetchone()
    if not check1:
        cur.execute("insert into order_status (name) values(?)",
                    ("Новый",))

    cur.execute("Select * From order_status where name=?", ('В работу',))
    check2 = cur.fetchone()
    if not check2:
        cur.execute("insert into order_status (name) values(?)",
                    ("В работу",))

    cur.execute("Select * From order_status where name=?",('На доставку',))
    check3 = cur.fetchone()
    if not check3:
        cur.execute("insert into order_status (name) values(?)",
                    ("На доставку",))

    cur.execute("Select * From order_status where name=?",('Доставлен',))
    check4 = cur.fetchone()
    if not check4:
        cur.execute("insert into order_status (name) values(?)",
                    ("Доставлен",))

    cur.execute("Select * From order_status where name=?",('Оплачен',))
    check4 = cur.fetchone()
    if not check4:
        cur.execute("insert into order_status (name) values(?)",
                    ("Оплачен",))

    conn.commit()
    conn.close()


def create_table_orders():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sum FLOAT CHECK (Sum >= 0),
    status_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(status_id) REFERENCES order_status(id))
    ''')

    conn.commit()
    conn.close()


def create_table_order_position():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            dishes_id INTEGER NOT NULL,  
            count INT DEFAULT 1,
            temp_sum FLOAT CHECK (temp_sum >= 0), 
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(dishes_id) REFERENCES dishes(id) 
        )
    ''')

    conn.commit()
    conn.close()
def add_dishes(Category, name, price, image):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute("insert into dishes(category_id, name, price, image) values(?,?,?,?)",
                (Category,name,price,image))
    conn.commit()
    conn.close()

def add_user_role():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute("Select * From user_role where name='Админ'")
    check1 = cur.fetchone()
    if not check1:
        cur.execute("insert into user_role (name, role) values(?,?)",
                ("Админ","Админ"))

    cur.execute("Select * From user_role where name='Повар'")
    check2 = cur.fetchone()
    if not check2:
        cur.execute("insert into user_role (name, role) values(?,?)",
                ("Повар","Повар"))

    cur.execute("Select * From user_role where name='Доставщик'")
    check3 = cur.fetchone()
    if not check3:
        cur.execute("insert into user_role (name, role) values(?,?)",
                ("Доставщик","Доставщик"))

    cur.execute("Select * From user_role where name='Клиент'")
    check4 = cur.fetchone()
    if not check4:
        cur.execute("insert into user_role (name, role) values(?,?)",
                ("Клиент","Клиент"))

    conn.commit()
    conn.close()

def user_change(user_name, phone, address):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('Select * From Users where name = ?',(user_name,))
    check1 = cur.fetchone()
    if check1:
        cur.execute("UPDATE Users SET phone = ?, address = ? WHERE name = ?", (phone, address, user_name))
    conn.commit()
    conn.close()

def add_order(user_name):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('Select id From order_status where name=?', ("Новый",))
    check2 = cur.fetchone()
    if check2:
        check2 = check2[0]
    else:
        print("Нет такого статуса")


    cur.execute('Select id From Users where name=?',(user_name,))
    check1 = cur.fetchone()
    if check1:
        check1 = check1[0]
    else:
        print("Нет такого юзера")

    if check1 and check2:
        cur.execute("INSERT INTO orders (user_id, status_id) VALUES (?, ?)",
                    (check1, check2))
        order_id = cur.lastrowid  # Получение ID нового заказа
        conn.commit()
        print(f"Заказ добавлен. ID нового заказа: {order_id}")
        return order_id

    else:
        print("Не удалось добавить заказ: отсутствует ID пользователя или статуса.")
    #conn.commit()
    conn.close()

def add_order_position(order_id, dishes_id, count):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute("Select price From dishes Where id = ?",(dishes_id,))
    price1 = cur.fetchone()
    if price1:
        price1 = price1[0]
    temp_sum = price1*count
    cur.execute("insert into order_positions (order_id, dishes_id, count, temp_sum) values(?,?,?,?)",
                (order_id, dishes_id, count, temp_sum))
    conn.commit()
    conn.close()

# создание таблицы отзывов о блюде
def create_table_feedback():
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS feedback 
        (id INTEGER PRIMARY KEY, 
        dishes TEXT NOT NULL, 
        user TEXT NOT NULL, 
        content TEXT NOT NULL, 
        raiting INTEGER, 
        FOREIGN KEY(user) REFERENCES (user.id) 
        FOREIGN KEY(dishes) REFERENCES (dishes.id)
        )
    ''')
    conn.commit()
    conn.close()

def add_feedback(dishes, user, content):
    rating = get_rating()
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (dishes, user, content, rating) VALUES (?, ?, ?, ?)", (dishes, user, content, rating))
    conn.commit()
    conn.close()

def get_rating():
    while True:
        rating = input("Введите рейтинг от 1 до 5: ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            return int(rating)
        else:
            print("Неверный ввод. Пожалуйста, введите число от 1 до 5.")

create_db_and_table()
create_table_users()
create_table_category()
create_table_status()
create_table_dishes()
create_table_orders()
create_table_order_position()
add_user_role()

Category = 1
name = "еда1"
price = 100
image = "ссылка на рисунок"

#add_dishes(Category, name, price, image)

user_name = "@Kvitov_Evgeny"
phone = '89997776655'
address = 'tyumen'

#user_change(user_name, phone, address)
order_id = add_order(user_name)

add_order_position(order_id,1,2)