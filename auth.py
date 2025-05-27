# auth.py
import hashlib
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_master_password():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS settings (master_hash TEXT)')
    c.execute('SELECT * FROM settings')
    if not c.fetchone():
        master = input("Create Master Password: ")
        c.execute('INSERT INTO settings VALUES (?)', (hash_password(master),))
        conn.commit()
    conn.close()

def verify_master_password(input_password):
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('SELECT master_hash FROM settings')
    data = c.fetchone()
    conn.close()
    if data:
        return hash_password(input_password) == data[0]
    return False

