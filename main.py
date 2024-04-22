import sqlite3
import telebot

conn = sqlite3.connect("zero_order_service.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)""")

conn.commit()
conn.close()

