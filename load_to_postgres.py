# load/load_to_postgres.py

import os
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(df, table_name):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id) DO NOTHING;
        """
        row_values = [json.dumps(val) if isinstance(val, (dict, list)) else val for val in row]
        cursor.execute(sql, row_values)

    conn.commit()
    cursor.close()
    conn.close()
