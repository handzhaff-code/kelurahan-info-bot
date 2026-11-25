# Module and Library
import os
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

# Code
def database_connection():
    try:
        load_dotenv()

        db_host = os.getenv("DB_HOST")
        db_port = int(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")

        print("[DB] Connecting to PostgreSQL...")

        connection = psycopg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
        print("[DB] Connecting successfully")
        register_vector(connection)
        print("[DB] pgvector registered successfully!")
        return connection
    except Exception:
        raise

if __name__ == "__main__":
    pass