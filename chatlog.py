import os
import json
from datetime import datetime

CHATLOG_FILE = "chatlog.json"

def load_chatlog():
    if os.path.exists(CHATLOG_FILE):
        with open(CHATLOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chatlog(chatlog):
    with open(CHATLOG_FILE, "w") as f:
        json.dump(chatlog, f, indent=4)

def append_chatlog(prompt, response):
    date = datetime.now().strftime("%Y-%m-%d")
    chatlog = load_chatlog()

    if date not in chatlog:
        chatlog[date] = []

    chatlog[date].append({
        "prompt": prompt,
        "response": response
    })

    save_chatlog(chatlog)
