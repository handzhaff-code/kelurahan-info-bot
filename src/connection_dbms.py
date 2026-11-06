# Module and Library
import os
import psycopg
from dotenv import load_dotenv

# Code
def database_connection():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = int(os.getenv("DB_PORT"))
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")

    connection = psycopg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    return connection

if __name__ == "__main__":
    connection = database_connection()
    connectionClosed = connection.close()

    print(connection.closed)