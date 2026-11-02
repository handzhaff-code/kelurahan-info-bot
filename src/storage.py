import json
import os
import models

# Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWLEDGE_JSON = os.path.join(BASE_DIR, "data", "knowledge.json")
TELEGRAM_STATE = os.path.join(BASE_DIR, "data", "telegram_state.json")

def json_Load():
    with open(KNOWLEDGE_JSON, "r", encoding="utf-8") as file:
        file_JSON = json.load(file)
        return file_JSON

def json_Save():
    pass

def dict_Loop():

    resultLoad = json_Load()
    objectResult = []

    for data in resultLoad:
        article = models.Article.from_dict(data)
        objectResult.append(article)

    return objectResult

def load_offset():
    with open(TELEGRAM_STATE, "r", encoding="utf-8") as file:
        result = json.load(file)
        offset = result["offset"]
        return offset

def save_offset(offset):
    state = {
        "offset" : offset
    }
    with open(TELEGRAM_STATE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)

'''if __name__ == "__main__":
    print(load_offset())'''