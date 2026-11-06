# This only for migration from json !!
import json
import pprint
from storage import KNOWLEDGE_JSON
from connection_dbms import database_connection

def json_to_dict(data):
    with open(data, "r", encoding="utf-8") as files:
        data_json = json.load(files)

        return data_json
    
def to_database(data_dict):
    connection = database_connection()
    cursor = connection.cursor()

    query_to_categories ="""
    insert into categories (name)
    values (%s)
    on conflict (name)
    do update set name = excluded.name
    returning id 
    """ 
    query_to_articles = """
    insert into articles (id, category_id, question, keywords, answer)
    values (%s, %s, %s, %s, %s)
    on conflict (id)
    do nothing
    """

    for data in data_dict:
        data_id = data["id"]
        data_category = data["category"]
        data_question = data["question"]
        data_keywords = data["keywords"]
        data_answer = data["answer"]

        cursor.execute(query_to_categories, (data_category,))
        category_id = cursor.fetchone()[0]

        cursor.execute(query_to_articles, (data_id, category_id, data_question, data_keywords, data_answer))

    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    data = json_to_dict(KNOWLEDGE_JSON)
    to_database(data)