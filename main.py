import sqlite3
import telebot
from telebot import TeleBot, types
from yookassa import Configuration, Payment

temp_storage = {}

# Конфигурация ЮKassa
shop_id = '371138'
secret_key = 'test_fo-_hU2Yy5bRR8GKE1K-B8hcGXWq4Jnf6fCIZrQPzHE'
Configuration.account_id = shop_id
Configuration.secret_key = secret_key

# Токен бота
TOKEN = '6788073016:AAELeQLwR7HMYSPuPwzo2XapRFHJxD55NTw'
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

# def add_user(name, role=None):
#     # Если роль не указана, автоматически присваиваем роль "клиент"
#     if role is None:
#         role = 'клиент'
#
#     try:
#         conn = sqlite3.connect('zero_order_service.db')
#         cursor = conn.cursor()
#
#         cursor.execute('INSERT INTO Users (name, user_role) VALUES (?, ?)', (name, role))
#         conn.commit()
#         conn.close()
#     except sqlite3.Error as e:
#         print(f"Ошибка при добавлении пользователя: {e}")
#     #finally:

def add_user(user_id, name, role=None):
    if role is None:
        role = 'клиент'
    try:
        conn = sqlite3.connect('zero_order_service.db')
        cursor = conn.cursor()
        # Проверка наличия пользователя в базе
        cursor.execute('SELECT * FROM Users WHERE user_id=?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO Users (user_id, name, user_role) VALUES (?, ?, ?)', (user_id, name, role))
            conn.commit()
            print("Пользователь успешно добавлен")
        else:
            print("Пользователь уже существует")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()

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
        user_id INTEGER,
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

def add_order(user_id):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('Select id From order_status where name=?', ("Новый",))
    check2 = cur.fetchone()
    if check2:
        check2 = check2[0]
    else:
        print("Нет такого статуса")


    cur.execute('Select id, user_id From Users where user_id=?',(user_id,))
    check1 = cur.fetchone()
    if check1:
        check1 = check1[0]
    else:
        print("Нет такого юзера")

    cur.execute('Select id From orders where user_id=? and status_id=?', (check1,check2))
    check3 = cur.fetchone()
    if check3:
        check3 = check3[0]
    else:
        print("Нет такого юзера")

    if check1 and check2 and not check3:
        cur.execute("INSERT INTO orders (user_id, status_id) VALUES (?, ?)",
                    (check1, check2))
        order_id = cur.lastrowid  # Получение ID нового заказа
        conn.commit()
        print(f"Заказ добавлен. ID нового заказа: {order_id}")
        return order_id
    elif check1 and check2 and check3:

        print(f"уже имеется заказ со статусом 'Новый': {check3}")
        return check3

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
    id = cur.fetchone()
    if id:
        id = id[0]
    conn.commit()
    conn.close()
    return id

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
    user_id = message.from_user.id
    user_name = message.from_user.full_name  # Получаем имя пользователя из данных Telegram
    # Регистрируем пользователя
    add_user(user_id, user_name)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Новый заказ', callback_data='new_order')
    itembtn2 = types.InlineKeyboardButton('Мои заказы', callback_data='my_orders')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, f"Привет, {user_name}! Чем могу помочь?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'start_back')
def handle_query(call):
    user_id = call.from_user.id  # Определяем user_id из данных запроса
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Новый заказ', callback_data='new_order')
    itembtn2 = types.InlineKeyboardButton('Мои заказы', callback_data='my_orders')
    markup.add(itembtn1, itembtn2)

    # Используем call.message.chat.id чтобы отправить сообщение в правильный чат
    bot.send_message(call.message.chat.id, "Привет! Чем могу помочь?", reply_markup=markup)

    # Не забудьте подтвердить обработку callback-запроса
    bot.answer_callback_query(call.id)

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
    user_id = call.from_user.id  # Определяем user_id из данных запроса
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
        conn = sqlite3.connect('zero_order_service.db')
        cur = conn.cursor()

        # Проверяем существование профиля пользователя в системе
        cur.execute('SELECT id FROM Users WHERE user_id=?', (user_id,))
        user_record = cur.fetchone()
        if not user_record:
            bot.send_message(call.message.chat.id, "У вас нет профиля в системе.")
            return

        # Получаем заказы пользователя
        cur.execute('Select id, user_id From Users where user_id=?', (user_id,))
        check1 = cur.fetchone()
        if check1:
            check1 = check1[0]  # определили id юзера с данным user_id
        else:
            print("Нет такого юзера")


        cur.execute('SELECT * FROM Orders WHERE user_id=?', (check1,))
        list_of_orders = cur.fetchall()

        if list_of_orders:
            markup = types.InlineKeyboardMarkup()
            for order_id, _, sum, _, order_name in list_of_orders:
                callback_data = f'myorder_{order_id}'
                button_text = f"от {order_name} на {sum} руб."
                markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
            back_button = types.InlineKeyboardButton("Назад к выбору", callback_data=f'start_back')
            markup.add(back_button)
            bot.send_message(call.message.chat.id, "Ваши заказы:", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "У вас нет активных заказов.")

        bot.answer_callback_query(call.id)  # Ответ на callback_query

        conn.close()  # Не забудьте закрыть соединение с базой данных

@bot.callback_query_handler(func=lambda call: call.data.startswith('myorder_'))
def order_position_select(call):
    order_id = call.data.split("_")[1]
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('Select * '
                'From order_positions as op '
                'join dishes as dd '
                'on op.dishes_id = dd.id '
                'where op.order_id=?', (order_id,))
    positions = cur.fetchall()
    if positions:
        markup = types.InlineKeyboardMarkup()
        for item in positions: #.id, op.order_id, op.dishes_id, op.count, op.temp_sum, dd.name in positions:
            name = item[6]
            button_text = f"{item[6]} {item[4]} - {item[3]} шт."
            # Создаем кнопку для позиции
            pos_button = types.InlineKeyboardButton(button_text, callback_data=f'pos_{id}')
            # Создаем кнопку для изменения количества
            change_button = types.InlineKeyboardButton("Изменить", callback_data=f'change_{id}')
            # Создаем кнопку для удаления позиции
            delete_button = types.InlineKeyboardButton("Удалить", callback_data=f'delete_{id}')
            # Добавляем кнопки в одной строке
            markup.row(pos_button, change_button, delete_button)
        # Добавляем кнопку "Назад к заказам"
        back_button = types.InlineKeyboardButton("Назад к заказам", callback_data=f'myorders_back_{order_id}')
        pay_button = types.InlineKeyboardButton("Оплатить заказ", callback_data=f'pay_order_{order_id}')
        markup.add(back_button)
        markup.add(pay_button)

        bot.send_message(call.message.chat.id, "Позиции в Вашем заказе:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "У вас нет активных заказов.")

    bot.answer_callback_query(call.id)
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_'))
def prompt_change_quantity(call):
    pos_id = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, "Введите новое количество:")
    bot.register_next_step_handler(msg, process_quantity_change, pos_id, call)

def process_quantity_change(message, pos_id, call):
    try:
        quantity = int(message.text)
        update_order_position(pos_id, quantity, db_name='zero_order_service.db')
        bot.send_message(message.chat.id, "Количество успешно обновлено!")
        conn = sqlite3.connect('zero_order_service.db')
        cur = conn.cursor()
        cur.execute('Select order_id From order_positions where id=?', (pos_id,))
        order_id = cur.fetchone()[0]
        cur.execute('Select * '
                    'From order_positions as op '
                    'join dishes as dd '
                    'on op.dishes_id = dd.id '
                    'where op.order_id=?', (order_id,))
        positions = cur.fetchall()
        if positions:
            markup = types.InlineKeyboardMarkup()
            for item in positions:  # .id, op.order_id, op.dishes_id, op.count, op.temp_sum, dd.name in positions:
                name = item[6]
                button_text = f"{item[6]} {item[4]} - {item[3]} шт."
            pos_button = types.InlineKeyboardButton(button_text, callback_data=f'pos_{id}')
            change_button = types.InlineKeyboardButton("Изменить", callback_data=f'change_{id}')
            delete_button = types.InlineKeyboardButton("Удалить", callback_data=f'delete_{id}')
            markup.row(pos_button, change_button, delete_button)
        back_button = types.InlineKeyboardButton("Назад к заказам", callback_data=f'myorders_back_{order_id}')
        markup.add(back_button)
        pay_button = types.InlineKeyboardButton("Оплатить заказ", callback_data=f'pay_order_{order_id}')
        markup.add(pay_button)
        bot.send_message(call.message.chat.id, "Позиции в Вашем заказе:", reply_markup=markup)
        conn.close()
        bot.answer_callback_query(call.id)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")


def update_order_position(pos_id, quantity, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("select dishes_id from order_positions where id = ?", (pos_id,))
    dishes_id = cur.fetchone()
    if dishes_id:
        dishes_id = dishes_id[0]
    cur.execute("select price from dishes where id = ?", (dishes_id,))
    price = cur.fetchone()
    if price:
        price = int(price[0])
    temp_sum = price * int(quantity)
    cur.execute("UPDATE order_positions SET count = ?, temp_sum = ? WHERE id = ?", (quantity, temp_sum, pos_id))
    conn.commit()
    cur.execute('Select order_id from order_positions where id=?', (pos_id,))
    check3 = cur.fetchone()
    if check3:
        check3 = check3[0]
        cur.execute("SELECT SUM(temp_sum) FROM order_positions WHERE order_id = ?", (check3,))
        summa = cur.fetchone()
        if summa:
            summa = summa[0]
        cur.execute('UPDATE orders SET sum = ? WHERE id = ?', (summa, check3))
        conn.commit()


    conn.commit()
    conn.close()


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def delete_order_position(call):
    pos_id = call.data.split("_")[1]
    # Здесь ваш код для удаления позиции
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('Select order_id From order_positions where id=?', (pos_id,))
    order_id = cur.fetchone()
    if order_id:
        order_id = order_id[0]

    delete_order_position(pos_id, db_name='zero_order_service.db')
    cur.execute('Select * '
                'From order_positions as op '
                'join dishes as dd '
                'on op.dishes_id = dd.id '
                'where op.order_id=?', (order_id,))
    positions = cur.fetchall()
    if positions:
        markup = types.InlineKeyboardMarkup()
        for item in positions:  # .id, op.order_id, op.dishes_id, op.count, op.temp_sum, dd.name in positions:
            name = item[6]
            button_text = f"{item[6]} {item[4]} - {item[3]} шт."
            # Создаем кнопку для позиции
            pos_button = types.InlineKeyboardButton(button_text, callback_data=f'pos_{id}')
            # Создаем кнопку для изменения количества
            change_button = types.InlineKeyboardButton("Изменить", callback_data=f'change_{id}')
            # Создаем кнопку для удаления позиции
            delete_button = types.InlineKeyboardButton("Удалить", callback_data=f'delete_{id}')
            # Добавляем кнопки в одной строке
            markup.row(pos_button, change_button, delete_button)
        # Добавляем кнопку "Назад к заказам"
        back_button = types.InlineKeyboardButton("Назад к заказам", callback_data=f'myorders_back_{order_id}')
        markup.add(back_button)
        pay_button = types.InlineKeyboardButton("Оплатить заказ", callback_data=f'pay_order_{order_id}')
        markup.add(pay_button)
        bot.send_message(call.message.chat.id, "Позиции в Вашем заказе:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "У вас нет активных заказов.")
    conn.close()
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('myorders_back_'))
def go_back_to_order_positions(call):
    order_id = call.data.split("_")[2]
    # Здесь ваш код для возврата к списку позиций заказа
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    user_id = call.from_user.id  # Определяем user_id из данных запроса
    # Проверяем существование профиля пользователя в системе
    cur.execute('SELECT id FROM Users WHERE user_id=?', (user_id,))
    user_record = cur.fetchone()
    if not user_record:
        bot.send_message(call.message.chat.id, "У вас нет профиля в системе.")
        return

    # Получаем заказы пользователя
    cur.execute('Select id, user_id From Users where user_id=?', (user_id,))
    check1 = cur.fetchone()
    if check1:
        check1 = check1[0]  # определили id юзера с данным user_id
    else:
        print("Нет такого юзера")

    cur.execute('SELECT * FROM Orders WHERE user_id=?', (check1,))
    list_of_orders = cur.fetchall()

    if list_of_orders:
        markup = types.InlineKeyboardMarkup()
        for order_id, _, sum, _, order_name in list_of_orders:
            callback_data = f'myorder_{order_id}'
            button_text = f"от {order_name} на {sum} руб."
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        back_button = types.InlineKeyboardButton("Назад к выбору", callback_data=f'start_back')
        markup.add(back_button)
        bot.send_message(call.message.chat.id, "Ваши заказы:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "У вас нет активных заказов.")

    bot.answer_callback_query(call.id)  # Ответ на callback_query

    conn.close()  # Не забудьте закрыть соединение с базой данных

    #bot.answer_callback_query(call.id)

# Обработка выбора категории
# Обработка выбора категории
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def category_selected(call):
    # Извлекаем ID категории из callback_data
    category_id = call.data.split('_')[1]
    #bot.send_message(call.message.chat.id, f"выбран id {category_id}")
    products = get_products_by_category(category_id)
    markup = types.InlineKeyboardMarkup()
    # Добавляем кнопки для каждого продукта
    for product_id, product_name in products:
        callback_data = f'product_{product_id}'
        markup.add(types.InlineKeyboardButton(product_name, callback_data=callback_data))
    bot.send_message(call.message.chat.id, "Выберите продукт:", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def product_selected(call):
    global temp_storage
    user_id = call.from_user.id
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM Users WHERE user_id=?', (user_id,))
    user_record = cur.fetchone()
    if user_record:
        user_record = user_record[0]

    product_id = call.data.split('_')[1]

    # Сохраняем выбранный продукт во временное хранилище (например, в словаре)
    temp_storage[user_record] = {'product_id': product_id}

    # Запрашиваем у пользователя количество
    msg = bot.send_message(call.message.chat.id, "Введите количество товара, которое вы хотите добавить:")
    bot.register_next_step_handler(msg, process_quantity, user_record, temp_storage, user_id)
    bot.answer_callback_query(call.id)

def process_quantity(message, user_record, temp_storage, user_id):
    #temp_storage = {}
    try:
        quantity = int(message.text)  # Преобразуем введённое значение в число
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        return
    if user_record in temp_storage:
        product_id = temp_storage[user_record]['product_id']
        order_id = add_order(user_id)  # Функция для получения или создания нового заказа

        # Добавляем продукт в заказ с указанным количеством
        add_order_position(order_id, product_id, quantity)

        # Убираем информацию о продукте из временного хранилища
        del temp_storage[user_record]

        markup = types.InlineKeyboardMarkup()
        finish_button = types.InlineKeyboardButton("Завершить заказ", callback_data='finish_order')
        add_more_button = types.InlineKeyboardButton("Добавить товар", callback_data='new_order')
        markup.add(add_more_button, finish_button)

        bot.send_message(message.chat.id, "Продукт добавлен в ваш заказ. Добавьте еще или завершите заказ.",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова.")
        return


@bot.callback_query_handler(func=lambda call: call.data == 'add_more')
def add_more_products(call):
    user_id = call.from_user.id
    # Здесь можно вызвать функцию, которая предложит пользователю повторно выбрать категорию продукта
    add_order_position(user_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'finish_order')
def finish_order(call):
    user_id = call.from_user.id
    complete_order(user_id)  # Функция, которая изменяет статус заказа на "Завершен"
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Новый заказ', callback_data='new_order')
    itembtn2 = types.InlineKeyboardButton('Мои заказы', callback_data='my_orders')
    markup.add(itembtn1, itembtn2)
    bot.send_message(call.message.chat.id, "Ваш заказ завершен и скоро будет обработан.", reply_markup=markup)

def complete_order(user_id):
    conn = sqlite3.connect('zero_order_service.db')
    cur = conn.cursor()

    cur.execute('Select id From order_status where name=?', ("Новый",))
    check2 = cur.fetchone()
    if check2:
        check2 = check2[0] #пределили id статуса "Новый"
    else:
        print("Нет такого статуса")

    cur.execute('Select id From order_status where name=?', ("В работу",))
    check4 = cur.fetchone()
    if check4:
        check4 = check4[0] #определили id статуса "В работу"
    else:
        print("Нет статуса В работу")

    cur.execute('Select id, user_id From Users where user_id=?', (user_id,))
    check1 = cur.fetchone()
    if check1:
        check1 = check1[0] #определили id юзера с данным user_id
    else:
        print("Нет такого юзера")

    #Находим заказ по данному юзеру со статусом новый, и меняем статус заказа
    cur.execute('Select id From orders where user_id=? and status_id=?', (check1, check2))
    check3 = cur.fetchone()
    if check3:
        check3 = check3[0]
        cur.execute("SELECT SUM(temp_sum) FROM order_positions WHERE order_id = ?", (check3,))
        summa = cur.fetchone()
        if summa:
            summa = summa[0]
        cur.execute('UPDATE orders SET status_id = ?, sum = ? WHERE id = ?', (check4, summa, check3))
        conn.commit()
        print('оменяли статус заказа на "В работу"')
    else:
        print("Нет такого юзера")

    conn.close()


def get_products_by_category(category_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM dishes WHERE category_id=?",(category_id,))
    products = cursor.fetchall()
    conn.close()
    return products


def delete_order_position(order_position_id, db_name='database.db'):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Удаляем запись из таблицы Order_position по id
        cursor.execute('DELETE FROM order_positions WHERE id = ?', (order_position_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print("Запись не найдена.")
        else:
            print("Запись успешно удалена.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении записи: {e}")
    finally:
        conn.close()


#def update_order_position(order_position_id, quantity, db_name='database.db'):
    # try:
    #     conn = sqlite3.connect(db_name)
    #     cursor = conn.cursor()
    #
    #     # Обновляем количество в позиции заказа
    #     cursor.execute('UPDATE order_positions SET quantity = ? WHERE id = ?', (quantity, order_position_id))
    #     conn.commit()
    #     if cursor.rowcount == 0:
    #         print("Запись не найдена.")
    #     else:
    #         print("Количество успешно обновлено.")
    # except sqlite3.Error as e:
    #     print(f"Ошибка при обновлении записи: {e}")
    # finally:
    #     conn.close()
    #

def manage_order_position(order_position_id):
    action = input("Введите 'удалить' для удаления позиции или 'изменить' для изменения количества: ").strip().lower()
    if action == 'удалить':
        delete_order_position(order_position_id)
    elif action == 'изменить':
        quantity = int(input("Введите новое количество: "))
        update_order_position(order_position_id, quantity)
    else:
        print("Некорректный ввод. Пожалуйста, введите 'удалить' или 'изменить'.")

def create_payment(amount, currency, return_url, description):
    """ Создать платеж через ЮKassa и возвратить объект платежа или None при ошибке. """
    try:
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description
        })
        return payment
    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")
        return None

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_order_"))
def handle_payment(call):
    order_id = call.data.split("_")[1]
    chat_id = call.message.chat.id
    amount = "10.00"  # Сумма к оплате, получите из данных заказа
    currency = "RUB"
    return_url = "https://your-return-url.com"  # URL, куда пользователь будет перенаправлен после оплаты
    description = f"Оплата заказа №{order_id}"

    payment = create_payment(amount, currency, return_url, description)
    if payment:
        # Перенаправляем пользователя на страницу оплаты
        payment_url = payment.confirmation.get('confirmation_url')
        bot.send_message(chat_id, f"Пожалуйста, перейдите по ссылке для оплаты: {payment_url}")
    else:
        bot.send_message(chat_id, "Произошла ошибка при создании платежа. Пожалуйста, попробуйте еще раз.")
    bot.answer_callback_query(call.id)

# ------  Начала кода примера оплаты
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     pay_button = types.KeyboardButton('Оплатить')
#     markup.add(pay_button)
#     bot.send_message(message.chat.id, "Для оплаты нажмите кнопку 'Оплатить'", reply_markup=markup)
#
# @bot.message_handler(func=lambda message: message.text == "Оплатить")
# def handle_payment(message):
#     amount = "100.00"  # Сумма платежа
#     currency = "RUB"  # Валюта платежа
#     return_url = "https://t.me/ForPG_bot"  # URL возврата
#     description = f"Платеж на {amount} руб."  # Формируем описание с использованием f-string
#
#     payment = create_payment(amount, currency, return_url, description)
#     if payment and payment.confirmation and payment.confirmation.confirmation_url:
#         markup = types.InlineKeyboardMarkup()
#         pay_button = types.InlineKeyboardButton('Перейти к оплате', url=payment.confirmation.confirmation_url)
#         markup.add(pay_button)
#         bot.send_message(message.chat.id, "Перейдите по ссылке для оплаты:", reply_markup=markup)
#     else:
#         bot.send_message(message.chat.id, "Не удалось создать платеж, пожалуйста, попробуйте позже.")
# ------ Конец код примера оплаты

create_db_and_table()
create_table_users()
create_table_category()
create_table_status()
create_table_dishes()
create_table_orders()
create_table_order_position()
create_table_feedback()
add_user_role()

#add_dishes(Category, name, price, image)
#user_change(user_name, phone, address)
# Запуск бота
bot.polling(none_stop=True)

