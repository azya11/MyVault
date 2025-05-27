# ui/login_ui.py
import tkinter as tk
from tkinter import messagebox
from auth import verify_master_password
from encryption import generate_key
from ui.vault_ui import open_vault_ui

def start_login_ui():
    def handle_login():
        password = entry.get()
        if verify_master_password(password):
            root.destroy()
            key = generate_key(password)
            open_vault_ui(key)
        else:
            messagebox.showerror("Erroe", "Wrong Master Password")

    root = tk.Tk()
    root.title("Password Vault - Login")
    root.geometry("300x150")
    
    tk.Label(root, text="Enter Master Password:").pack(pady=10)
    entry = tk.Entry(root, show="*", width=30)
    entry.pack()
    
    tk.Button(root, text="Login", command=handle_login).pack(pady=10)
    
    root.mainloop()
