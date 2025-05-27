# main.py
from ui.login_ui import start_login_ui
from auth import init_master_password, init_security_table
from database import init_vault_db

if __name__ == "__main__":
    init_master_password()
    init_vault_db()
    init_security_table()
    start_login_ui()
