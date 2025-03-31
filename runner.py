import os
import sys
import json
from cryptography.fernet import Fernet

KEY_FILE = "encryption_key.bin"
DB_ENCRYPTED_PATH = "tools.json.enc"  # Updated path

def load_key():
    if not os.path.exists(KEY_FILE):
        print("Encryption key missing! Run encryptor.py first.")
        sys.exit(1)
    with open(KEY_FILE, "rb") as f:
        return f.read()

def decrypt_file(encrypted_file):
    key = load_key()
    
    if not os.path.exists(encrypted_file):
        print(f"Error: {encrypted_file} not found!")
        sys.exit(1)

    cipher = Fernet(key)

    with open(encrypted_file, "rb") as f:
        decrypted_data = cipher.decrypt(f.read())

    return decrypted_data

def decrypt_and_patch_json():
    if not os.path.exists(DB_ENCRYPTED_PATH):
        print("Error: Encrypted database not found!")
        sys.exit(1)

    decrypted_data = decrypt_file(DB_ENCRYPTED_PATH)
    tools_database = json.loads(decrypted_data.decode())

    class FakeFile:
        def __init__(self, data):
            self.data = data.encode()
        def read(self):
            return self.data
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    global open
    original_open = open

    def open_patched(file, mode="r", *args, **kwargs):
        if "tools.json" in file and "r" in mode:
            return FakeFile(json.dumps(tools_database))
        return original_open(file, mode, *args, **kwargs)

    globals()["open"] = open_patched
    print("Decrypted database injected into memory.")

if len(sys.argv) < 2:
    print("Usage: python runner.py <encrypted_script>")
    sys.exit(1)

file_name = sys.argv[1]

if file_name.endswith(".py.enc"):
    decrypt_and_patch_json()
    decrypted_code = decrypt_file(file_name)
    
    exec(decrypted_code, globals())
else:
    print("Invalid file type. Use an encrypted .py.enc file.")
