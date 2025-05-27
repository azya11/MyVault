# ui/add_entry_ui.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from encryption import encrypt_password

def open_add_entry_ui(fernet_key, refresh_callback):
    def save():
        site = entry_site.get()
        username = entry_username.get()
        password = entry_password.get()
        if not site or not username or not password:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        encrypted = encrypt_password(fernet_key, password)
        conn = sqlite3.connect("vault.db")
        c = conn.cursor()
        c.execute("INSERT INTO vault (site, username, password) VALUES (?, ?, ?)", (site, username, encrypted))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Entry added successfully.")
        window.destroy()
        refresh_callback()

    window = tk.Toplevel()
    window.title("Add New Entry")
    window.geometry("300x200")

    tk.Label(window, text="Site:").pack(pady=5)
    entry_site = tk.Entry(window)
    entry_site.pack()

    tk.Label(window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(window)
    entry_username.pack()

    tk.Label(window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(window, show="*")
    entry_password.pack()

    tk.Button(window, text="Save", command=save).pack(pady=10)
