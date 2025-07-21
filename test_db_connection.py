# test_db_connection.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Connected to PostgreSQL successfully.")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()
