# database.py
import sqlite3

def init_vault_db():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            site TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

