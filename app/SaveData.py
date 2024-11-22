import json

SAVE_FILE = "./save.json"


INITIAL_SAVE_DATA = {
    "preferredModel":{
        "tokens": "4B",
        "vectors": "50d"
    }
}

def save_data(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(SAVE_FILE, "w") as file:
            json.dump(INITIAL_SAVE_DATA, file, indent=4)
        return INITIAL_SAVE_DATA
    except json.JSONDecodeError:
        return INITIAL_SAVE_DATA