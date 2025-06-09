import json
from pathlib import Path

USERS_FILE = Path("users.json")
CHAT_LOG_FILE = Path("chat_logs.json")

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def clear_chat():
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump({"messages": []}, f)

def load_chat():
    if CHAT_LOG_FILE.exists():
        with open(CHAT_LOG_FILE, 'r') as f:
            return json.load(f)
    return {"messages": []}

def save_chat(chat):
    with open(CHAT_LOG_FILE, 'w') as f:
        json.dump(chat, f, indent=4)
