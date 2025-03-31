import os
from cryptography.fernet import Fernet

KEY_FILE = "encryption_key.bin"
FILES_TO_ENCRYPT = ["jaydh.py", "scanner.py", "tools.json"]  # Updated path

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("Encryption key generated.")

def encrypt_file(file):
    if not os.path.exists(file):
        print(f"Error: {file} not found! Skipping...")
        return
    
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    
    cipher = Fernet(key)
    
    with open(file, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())

    enc_file = file + ".enc"
    with open(enc_file, "wb") as f:
        f.write(encrypted_data)
    
    os.remove(file)  # Delete original file
    print(f"Encrypted: {file} → {enc_file}")

generate_key()
for file in FILES_TO_ENCRYPT:
    encrypt_file(file)
