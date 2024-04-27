import sqlite3
import telebot
from telebot import types

# Токен бота
TOKEN = '6788073016:AAHjfoI1LAL49Ju0HJXEh8Lx8rGhlVVVVv4'
bot = telebot.TeleBot(TOKEN)

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
#     (id INTEGER PRIMARY KEY AUTOINCREMENT,
#     sum FLOAT CHECK (sum >= 0),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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

def update_table_dishes(dishes_id, category_id=None, name=None, price=None, image=None):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    # Создаем строку запроса с динамическим обновлением только тех полей, которые предоставлены
    update_query = "UPDATE dishes SET "
    update_values = []

    if category_id is not None:
        update_query += "category_id = ?, "
        update_values.append(category_id)
    if name is not None:
        update_query += "name = ?, "
        update_values.append(name)
    if price is not None:
        update_query += "price = ?, "
        update_values.append(price)
    if image is not None:
        update_query += "image = ?, "
        update_values.append(image)

        # Проверяем, были ли добавлены поля в запрос обновления
    if not update_values:
        print("Обновления не предоставлены.")
        return

    # Удаляем последнюю запятую и пробел из update_query
    update_query = update_query.rstrip(', ')
    update_query += " WHERE id = ?"
    update_values.append(dishes_id)

    # Выполняем обновление
    cur.execute(update_query, update_values)
    conn.commit()
    conn.close()
    print("Информация о блюде обновлена успешно.")

# Пример использования:
# update_dishes(1, category_id=2, name='Обновленное название', price=15.99, image='new_image.jpg')


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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        dishes INTEGER NOT NULL, 
        user INTEGER NOT NULL, 
        content TEXT NOT NULL, 
        rating INTEGER, 
        FOREIGN KEY(user) REFERENCES Users(id) 
        FOREIGN KEY(dishes) REFERENCES dishes(id)
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


# Подключение к базе данных
def connect_to_db():
    conn = sqlite3.connect('zero_order_service.db')
    return conn

# Получение категорий из базы данных
def get_categories():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category_name FROM Category_dishes")
    categories = cursor.fetchall()
    conn.close()
    return categories

# Обработка команды start
# Обработка команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Новый заказ', callback_data='new_order')
    itembtn2 = types.InlineKeyboardButton('Мои заказы', callback_data='my_orders')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Привет! Чем могу помочь?", reply_markup=markup)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'Новый заказ':
        categories = get_categories()
        markup = types.InlineKeyboardMarkup()
        for category_id, category_name in categories:
            callback_data = f'category_{category_id}'
            markup.add(types.InlineKeyboardButton(category_name, callback_data=callback_data))
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)
    elif message.text == 'Мои заказы':
        bot.send_message(message.chat.id, "Ваши заказы:")

# Обработка callback от inline кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'new_order' or call.data == 'my_orders')
def handle_query(call):
    if call.data == 'new_order':
        # Обработка выбора "Новый заказ"
        categories = get_categories()
        markup = types.InlineKeyboardMarkup()
        for category_id, category_name in categories:
            callback_data = f'category_{category_id}'
            markup.add(types.InlineKeyboardButton(category_name, callback_data=callback_data))
        bot.send_message(call.message.chat.id, "Выберите категорию:", reply_markup=markup)
    elif call.data == 'my_orders':
        # Обработка выбора "Мои заказы"
        bot.send_message(call.message.chat.id, "Ваши заказы:")
    bot.answer_callback_query(call.id)


# Обработка выбора категории
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def category_selected(call):
    # Извлекаем ID категории из callback_data
    category_id = call.data.split('_')[1]
    bot.send_message(call.message.chat.id, f"выбран id {category_id}")
    return category_id


create_db_and_table()
create_table_users()
create_table_category()
create_table_status()
create_table_dishes()
create_table_orders()
create_table_order_position()
create_table_feedback()
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

# Запуск бота
bot.polling(none_stop=True)