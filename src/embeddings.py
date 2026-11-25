# Library and module
from pprint import pprint
from pgvector import Vector
from llm import llm_embedding, llm_function
from telegram_api import telegram_API, get_Message
from storage import dict_Loop, updates_embeddings
from connection_dbms import database_connection
from search import build_context_vector, build_prompt_vector
# Code

def generate_doc_embeddings():
    object_Articles = dict_Loop()
    for article in object_Articles:
        id = article.id
        question = article.question
        answer = article.answer
        document = f"{question} {answer}"
        
        embedding_data = llm_embedding(document)
        updates_embeddings(id, embedding_data)

def generate_query_embedding(message):
    query_embedding = llm_embedding(message)
    return query_embedding

def pg_vector_consine_distance(query):
    query_consine_distance = """
    select 
    id,
    question,
    answer,
    embedding <=> %s as distance
    from articles
    where embedding is not null
    order by distance asc
    limit 5
    """
    try:
        connection = database_connection()
        cursor = connection.cursor()

        query_vector = Vector(query)

        # Already ordered by ASC low to high :3
        cursor.execute(query_consine_distance, (query_vector,))
        result = cursor.fetchall()

        return result
    except Exception :
        raise
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None: 
            connection.close()


if __name__ == "__main__":
    pass
    