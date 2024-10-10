import sqlite3 as sql
from sys import exit
from datetime import datetime


class Database:
    def __init__(self):
        self.result_default = 0
        self.result_finish = 1
        self.conn = sql.connect('database/database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY,
                              telegram_chat_id INTEGER,
                              telegram_user_id INTEGER,
                              day_regist INTEGER,
                              month_regist INTEGER,
                              year_regist INTEGER, 
                              hour_regist INTEGER,
                              minute_regist INTEGER,
                              second_regist INTEGER, 
                              win_count INTEGER DEFAULT 0,
                              lose_count INTEGER DEFAULT 0)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games
                             (id INTEGER PRIMARY KEY,
                              telegram_user_id INTEGER,
                              hidden_number INTEGER,
                              result INTEGER)''')

    def register_user(self, id_chat, id_user):
        date = datetime.now().date()
        time = datetime.now().time()
        self.cursor.execute('SELECT telegram_chat_id FROM users WHERE telegram_chat_id = ?', [id_chat])
        if self.cursor.fetchone() is None:
            self.cursor.execute(
                f'''INSERT INTO users(telegram_chat_id, telegram_user_id, day_regist, month_regist,
                 year_regist, hour_regist, minute_regist, second_regist) VALUES ({id_chat}, {id_user}, {date.day},
                {date.month}, {date.year}, {time.hour}, {time.minute}, {time.second})'''
            )
            self.conn.commit()

    def start_game(self, id_user, hidden_number):
        self.cursor.execute(
            f'''INSERT INTO games(telegram_user_id, hidden_number, result) VALUES ({id_user}, {hidden_number}, {self.result_default})'''
        )
        self.cursor.execute(
            f'''UPDATE users SET lose_count = lose_count + 1 WHERE telegram_user_id = {id_user}'''
        )
        self.conn.commit()

    def finish_game(self, id_user):
        self.cursor.execute(
            f'''SELECT id FROM games WHERE telegram_user_id = {id_user}'''
        )
        id_game = self.cursor.fetchall()[-1][0]
        self.cursor.execute(
            f'''UPDATE games SET result = {self.result_finish} WHERE id = {id_game}'''
        )
        self.conn.commit()

    def check_number(self, id_user):
        self.cursor.execute(
            f'''SELECT hidden_number FROM games WHERE telegram_user_id = {id_user}'''
        )
        return int(self.cursor.fetchall()[-1][0])

    def check_game(self, id_user):
        self.cursor.execute(
            f'''SELECT * FROM games WHERE telegram_user_id = {id_user} AND result = {self.result_default}'''
        )
        return self.cursor.fetchall()

    def user_win(self, id_user):
        self.cursor.execute(
            f'''UPDATE users SET win_count = win_count + 1 WHERE telegram_user_id = {id_user}'''
        )
        self.cursor.execute(
            f'''UPDATE users SET lose_count = lose_count - 1 WHERE telegram_user_id = {id_user}'''
        )

        self.conn.commit()

    def get_stats(self, id_user):
        self.cursor.execute(
            f'''SELECT win_count, lose_count FROM users WHERE telegram_user_id = {id_user}'''
        )
        return self.cursor.fetchone()


db = Database()
