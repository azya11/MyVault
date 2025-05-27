from ui.login_ui import start_login_ui
from auth import init_security_table
from database import init_vault_db

if __name__ == "__main__":
    init_vault_db()
    init_security_table()
    start_login_ui()
