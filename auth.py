import hashlib
import sqlite3
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def init_master_password():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS settings (master_hash TEXT)')
    c.execute('SELECT * FROM settings')
    if not c.fetchone():
        while True:
            master = input("Create Master Password: ")
            if is_strong(master):
                break
            else:
                print("Password too weak. Must contain at least:\n"
                      "- 8 characters\n- 1 uppercase letter\n- 1 lowercase letter\n- 1 digit\n- 1 special character (!@#$...)")
        c.execute('INSERT INTO settings VALUES (?)', (hash_password(master),))
        conn.commit()
        exit()
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

def init_security_table():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS security (id INTEGER PRIMARY KEY, attempts INTEGER)')
    c.execute('SELECT * FROM security')
    if not c.fetchone():
        c.execute('INSERT INTO security (attempts) VALUES (0)')
    conn.commit()
    conn.close()

def get_attempts():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute('SELECT attempts FROM security WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def increment_attempts():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute('UPDATE security SET attempts = attempts + 1 WHERE id = 1')
    conn.commit()
    conn.close()

def reset_attempts():
    conn = sqlite3.connect("vault.db")
    c = conn.cursor()
    c.execute('UPDATE security SET attempts = 0 WHERE id = 1')
    conn.commit()
    conn.close()
