import json
import os
from app.Config import SAVE_FILE

INITIAL_SAVE_DATA = {
    "setupComplete": False
}

def save_data(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return INITIAL_SAVE_DATA
    except json.JSONDecodeError:
        return INITIAL_SAVE_DATA