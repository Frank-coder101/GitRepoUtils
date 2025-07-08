import sqlite3
import os

DB_PATH = os.path.expanduser("~/.defihuddle_trading.db")

class Persistence:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        conn = Persistence.get_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS backtest_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy TEXT,
            result TEXT,
            timestamp TEXT
        )''')
        conn.commit()
        conn.close()

    @staticmethod
    def save_backtest_result(strategy, result):
        conn = Persistence.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO backtest_results (strategy, result, timestamp) VALUES (?, ?, datetime("now"))', (strategy, str(result)))
        conn.commit()
        conn.close()
