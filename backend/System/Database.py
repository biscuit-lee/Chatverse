import psycopg2
import os
from dotenv import load_dotenv

class Database:
    
    def __init__(self):
        load_dotenv()
        self.conn = None

    def get_db_connection(self):
        try:
            print("getting connection from db")
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.conn = conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None
    
    def get_connection(self):
        print("getting connection from db")
        if self.conn is None:
            self.get_db_connection()
        return self.conn
    def close(self):
        if self.conn:
            self.conn.close()