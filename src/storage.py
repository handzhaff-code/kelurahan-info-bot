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

# Backend storage database logic

def create_article(data):
    connection = database_connection()
    cursor = connection.cursor()

    query_to_articles = """INSERT into articles (id, category_id, question, keywords, answer)
        values (%s, %s, %s, %s, %s)
        on conflict (id)
        do nothing
        returning (id)
        """
    # For categories update or create we'll make their own reuseable function soon :3
    query_to_categories = """INSERT into categories (name)
        values (%s)
        on conflict (name)
        do update set name = excluded.name
        returning id 
        """
    
    id_ = data["id"]
    category_name = data["category"]
    question_ = data["question"]
    keywords_ = data["keywords"]
    answer_ = data["answer"]

    try:
        '''Execute for finding categories.name'''
        cursor.execute(query_to_categories, (category_name,))
        category_id = cursor.fetchone()[0]

        '''Then, execute for finding articles base on articles.id'''
        cursor.execute(query_to_articles, (id_, category_id, question_, keywords_, answer_))
        result_fetch = cursor.fetchone()
        # Result fetchone without indexing will be a tuple format (x,)

        '''validating database return none for ID already Exist, return ID for insert completed'''
        if result_fetch is None:
            connection.rollback()
            return False
        else:
            connection.commit()
            return True
        
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def updates_articles(data):
    # Adjust this input !!!
    connection = database_connection()
    cursor = connection.cursor()
    query_updates = """
    update articles
    set question = %s,
    answer = %s
    where id = %s
    """
    input_ID = data["id"]
    input_Question = data["question"]
    input_Answer = data["answer"]

    try:
        cursor.execute(query_updates, (input_Question, input_Answer, input_ID))

        if cursor.rowcount == 1:
            connection.commit()
            return True
        elif cursor.rowcount == 0:
            connection.rollback()
            return False
        else:
            connection.rollback()
        
    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def delete_articles_db(data):
    # Adjust this input !!! (FOR TESTING ONLY !!!)
    article_id = data
    connection = database_connection()
    cursor = connection.cursor()

    query_delete = """
    delete from articles 
    where id = %s
    """
    try:
        cursor.execute(query_delete, (article_id,))
        if cursor.rowcount == 1:
            connection.commit()
            return True
        elif cursor.rowcount == 0:
            connection.rollback()
            return False
    except Exception:
        raise
    finally:
        cursor.close()
        connection.close()

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
    
    cursor = connection.cursor(row_factory=dict_row) # We can set this row_factory into the dict, tuple, list or whatever you want (But cuz i already used dict data for convert to object Article)
    cursor.execute(query)

    data = cursor.fetchall()

    return data

def get_article(article_id):
    articles = get_all_article()

    for article in articles:
        if article["id"] == article_id:
            return article
        
    return None

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
    data = get_article("A001")
    pprint(data)