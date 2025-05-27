# encryption.py
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_password(key, password):
    return key.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    return key.decrypt(encrypted_password.encode()).decode()

