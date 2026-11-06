import json
import os
import models
from pprint import pprint
from connection_dbms import database_connection
from psycopg.rows import dict_row

# Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWLEDGE_JSON = os.path.join(BASE_DIR, "data", "knowledge.json")
TELEGRAM_STATE = os.path.join(BASE_DIR, "data", "telegram_state.json")

def get_all_article():
    query = """SELECT articles.id, 
    categories.name as category, 
    articles.question, 
    articles.keywords, 
    articles.answer
    from articles
    join categories
        ON category_id = categories.id;"""
    
    connection = database_connection()

    cursor = connection.cursor(row_factory=dict_row)
    cursor.execute(query)

    data = cursor.fetchall()

    return data


def json_Load():
    with open(KNOWLEDGE_JSON, "r", encoding="utf-8") as file:
        file_JSON = json.load(file)
        return file_JSON

def json_Save():
    pass

def dict_Loop():

    resultLoad = get_all_article()
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

if __name__ == "__main__":
    object = dict_Loop()
    pprint(object, sort_dicts=False)