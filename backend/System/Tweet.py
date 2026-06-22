import datetime
import psycopg2
import os
from dotenv import load_dotenv
import Database

# Timestamp, the tweeter, likes, replies(??)
class Tweet:
    def __init__(self, text, author_id, parent_tweet_id):
        self.text = text
        self.author_id = author_id
        self.timestamp = datetime.datetime.now()
        self.likes = 0
        self.comment_amount = 0
        self.parent_tweet_id = parent_tweet_id
        self.replies = []
        
    def add_likes(self):
        self.likes += 1

    def add_reply(self,reply):
        self.replies.append(reply)
        self.comment_amount += 1

    def send_to_db(self):
        db = Database()
        conn = db.get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        cursor.execute("insert into tweets (text, author_id, timestamp, likes, comment_amount, parent_tweet_id) values (%s, %s, %s, %s, %s, %s)", 
                       (self.text, self.author_id, self.timestamp, self.likes, self.comment_amount, self.parent_tweet_id))
        conn.commit()
        cursor.close()

    def get_text(self):
        return self.text
    
    def get_author_username(self):
        return self.author_username
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_likes(self):
        return self.likes
    
    def get_comment_amount(self):
        return self.comment_amount
    
    def get_replies(self):
        return self.replies
    
    
    def tweet(self):        
        self.send_to_db()


