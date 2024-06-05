import sqlite3
from datetime import datetime


class History:

    def get_add_history_by_id_from_card(self, lst):
        # Отримання історії додавання коштів з даних картки
        history_entries = []
        for entry in lst:
            if entry['amount'] < 0:
                dat = datetime.utcfromtimestamp(entry['time'])
                format_dat = dat.strftime("%Y %m-%d").replace(' 0', ' ')
                accounts = abs(entry['amount'] / 100.0)
            else:
                continue
            history_entries.append({'timestamp': format_dat, 'amount': accounts})

        return history_entries

    def get_m_history_by_id_from_card(self, lst):
        # Отримання історії поповнень коштів з даних картки
        history_entries = []
        for entry in lst:
            if entry['amount'] > 0:
                dat = datetime.utcfromtimestamp(entry['time'])
                format_dat = dat.strftime("%Y %m-%d").replace(' 0', ' ')
                accounts = abs(entry['amount'] / 100.0)
            else:
                continue
            history_entries.append({'timestamp': format_dat, 'amount': accounts})

        return history_entries


    def create_history_file_from_card(self, user_id, history_data):
        # Створення файлу з історією транзакцій для користувача з даних картки
        if history_data:
            with open(f'history_card_{user_id}.txt', 'w') as file:
                for entry in history_data:
                    if entry['amount'] < 0:
                        dat = datetime.utcfromtimestamp(entry['time'])
                        format_dat = dat.strftime("%Y-%m-%d %H:%M:%S")
                        accounts = entry['amount'] / 100.0
                        file.write(f"Дата: {format_dat}, Витрачено: {accounts}\n\n")
            return f'history_card_{user_id}.txt'
        else:
            return None


class Card:
    def __init__(self, db_name):
        # Ініціалізація підключення до бази даних і створення курсору
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Створення таблиці для збереження даних карток, якщо вона не існує
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    user_id INTEGER,
                    card_token TEXT,
                    user_card_id TEXT,
                    card_val TEXT
                )
            """)

    def get_user_card(self, user_id):
        # Отримання статусу картки користувача за user_id
        with self.conn:
            self.cur.execute("SELECT card_val FROM cards WHERE user_id = ?", (user_id, ))
            row = self.cur.fetchone()
            if row:
                return row[0]
            else:
                return False

    def get_user_card_data(self, user_id):
        # Отримання токену і ID картки користувача за user_id
        with self.conn:
            self.cur.execute("SELECT card_token, user_card_id FROM cards WHERE user_id = ?", (user_id, ))
            row = self.cur.fetchone()
            if row:
                return row[0], row[1]
            else:
                return 'None'

    def card_add(self, user_id, card, user_id_card, card_val='Не підключено'):
        # Додавання або оновлення даних картки користувача
        with self.conn:
            self.cur.execute("""
                SELECT user_id FROM cards WHERE user_id = ?
            """, (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                    UPDATE cards SET card_token = ?, user_card_id = ?, card_val = ? WHERE user_id = ?
                """, (card, user_id_card, card_val, user_id))
                return True
            else:
                self.cur.execute("INSERT INTO cards (user_id, card_token, user_card_id, card_val) VALUES (?, ?, ?, ?)",
                                 (user_id, card, user_id_card, card_val))
                return False

    def delete_card(self, user_id):
        # Видалення картки користувача, оновлюючи її статус на "Не підключено"
        with self.conn:
            self.cur.execute("UPDATE cards SET card_val = ? WHERE user_id = ?", ('Не підключено', user_id))

    def get_all_card_data(self):
        # Отримання всіх даних про картки користувачів
        with self.conn:
            self.cur.execute("SELECT * FROM cards")
            rows = self.cur.fetchall()
            if rows:
                return rows
            else:
                return 'None'
