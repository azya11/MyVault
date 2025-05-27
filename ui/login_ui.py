import tkinter as tk
from tkinter import messagebox
from auth import (
    verify_master_password,
    get_attempts,
    increment_attempts,
    reset_attempts,
    master_password_exists,
    save_master_password,
    is_strong
)
from encryption import generate_key
from ui.vault_ui import open_vault_ui
import sqlite3
import datetime

def log_event(message):
    with open("vault_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def show_login_ui():
    def handle_login():
        password = entry.get()

        if get_attempts() >= 10:
            messagebox.showerror("Vault Locked", "Too many failed attempts. Vault was wiped.")
            return

        if verify_master_password(password):
            reset_attempts()
            root.destroy()
            key = generate_key(password)
            open_vault_ui(key)
        else:
            increment_attempts()
            remaining = 10 - get_attempts()
            if remaining <= 0:
                conn = sqlite3.connect("vault.db")
                c = conn.cursor()
                c.execute("DELETE FROM vault")
                conn.commit()
                conn.close()
                log_event("Vault wiped due to 10 failed master password attempts.")
                messagebox.showerror("Vault Wiped", "Too many failed attempts. All data has been deleted.")
                root.destroy()
            else:
                messagebox.showerror("Wrong Password", f"Incorrect master password. Attempts left: {remaining}")

    root = tk.Tk()
    root.title("Password Vault - Login")
    root.geometry("300x150")

    tk.Label(root, text="Enter Master Password:").pack(pady=10)
    entry = tk.Entry(root, show="*", width=30)
    entry.pack()

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)

    root.mainloop()

def show_create_password_ui():
    def submit():
        pwd1 = entry1.get()
        pwd2 = entry2.get()
        if pwd1 != pwd2:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not is_strong(pwd1):
            messagebox.showerror("Weak Password", "Password must have:\n"
                                     "- 8+ characters\n- Uppercase\n- Lowercase\n- Digit\n- Special character")
            return
        save_master_password(pwd1)
        messagebox.showinfo("Success", "Master password created.")
        window.destroy()
        show_login_ui()

    window = tk.Tk()
    window.title("Create Master Password")
    window.geometry("300x200")

    tk.Label(window, text="Enter master password:").pack(pady=5)
    entry1 = tk.Entry(window, show="*")
    entry1.pack()

    tk.Label(window, text="Confirm password:").pack(pady=5)
    entry2 = tk.Entry(window, show="*")
    entry2.pack()

    tk.Button(window, text="Save", command=submit).pack(pady=10)

    window.mainloop()

def start_login_ui():
    if not master_password_exists():
        show_create_password_ui()
    else:
        show_login_ui()
