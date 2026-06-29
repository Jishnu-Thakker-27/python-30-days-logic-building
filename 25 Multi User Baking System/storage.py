import json
import os

USERS_FILE = "users.json"
BANKING_FILE = "banking_data.json"
TRANSACTIONS_FILE = "transactions.json"

def _load_data(filename, default_factory):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_factory(), f, indent=4)
        return default_factory()
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return default_factory()
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        # Backup corrupt file or just write default
        with open(filename, "w") as f:
            json.dump(default_factory(), f, indent=4)
        return default_factory()

def _save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def user_load():
    return _load_data(USERS_FILE, list)

def user_save(data):
    _save_data(USERS_FILE, data)

def banking_load():
    return _load_data(BANKING_FILE, dict)

def banking_save(data):
    _save_data(BANKING_FILE, data)

def transactions_load():
    return _load_data(TRANSACTIONS_FILE, dict)

def transactions_save(data):
    _save_data(TRANSACTIONS_FILE, data)