import sqlite3
import telebot

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

# Пример использования функций
create_db_and_table()  # Создаем базу данных и таблицу
add_category('Супы')  # Добавляем категорию 'Супы'
add_category('Гарниры')  # Добавляем категорию 'Гарниры'

