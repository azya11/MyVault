# ui/vault_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from encryption import decrypt_password
from ui.add_entry_ui import open_add_entry_ui

def open_vault_ui(fernet_key):
    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect("vault.db")
        c = conn.cursor()
        c.execute("SELECT rowid, site, username, password FROM vault")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            decrypted = decrypt_password(fernet_key, row[3])
            tree.insert('', 'end', iid=row[0], values=(row[1], row[2], decrypted))

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No choice available", "Choose entry to delete.")
            return
        rowid = selected[0]
        conn = sqlite3.connect("vault.db")
        c = conn.cursor()
        c.execute("DELETE FROM vault WHERE rowid = ?", (rowid,))
        conn.commit()
        conn.close()
        load_data()
        messagebox.showinfo("Deleted", "Entry was deleted.")

    def add_entry():
        open_add_entry_ui(fernet_key, load_data)

    root = tk.Tk()
    root.title("Password Vault")
    root.geometry("600x400")

    tree = ttk.Treeview(root, columns=("site", "username", "password"), show="headings")
    tree.heading("site", text="site")
    tree.heading("username", text="Username")
    tree.heading("password", text="Password")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add", command=add_entry).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_selected).pack(side=tk.LEFT, padx=5)

    load_data()
    root.mainloop()
