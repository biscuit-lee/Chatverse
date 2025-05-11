import psycopg2
import os
from dotenv import load_dotenv

class Database:
    
    def __init__(self):
        load_dotenv()
        self.conn = None

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            return conn

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
    def close(self):
        if self.conn:
            self.conn.close()