import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request

from scrapers import walmartScraper
import datetime
from System.Database import Database

app = Flask(__name__)

tweets = [{"id":1,"text":"HELLO CHAT", "author_id":1,"timestamp":"2003", "likes":1, "comment_amount":0,"parent_id":None},
            {"id":2,"text":"GDAY CHAT", "author_id":2,"timestamp":"2010", "likes":21, "comment_amount":1,"parent_id":None}
            ]

@app.route('/api/tweets',methods=["GET"])
def get_tweets():
    print("sending tweets")

    return jsonify(tweets)
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from the backend!'
    }
    return jsonify(data)

@app.route('/api/login',methods=["POST"])
def login_verify():
    if request.method == "POST":
        
        db = Database()
        conn = db.get_connection()
        
        if conn is None:
            return jsonify({"message :" "FAILED to connect to database"},500)
        
        data = request.get_json()
        username = data['username']
        password = data['password']
        print(f"EYO BOSS WE GOT A HOME BOY CALLED {username} with pass {password}")
        query = "SELECT * from users where username = 'john' AND passhash ='123' "
        try:
            curr = conn.cursor()
            curr.execute(query)
            res = curr.fetchone()
            print("FETCHIN the user")
            if res:
                print("WE FOUND THE HOMEBOY")
                return jsonify({"message ": "Logged in successfully "}),200
            else:
                print("WE AINT FIND THE HOMEBOY")
                return jsonify({"message ": "Login failed , Cannot find user "}),401
                
            
        except Exception as e:
            
            print(f"SOMETHING WRONG ABOUT THE QUERY : {e}")
            return (jsonify({"message" : f"error during query {str(e)}"},500))

        finally:
            db.close()

if __name__ == '__main__':
    app.run(debug=True)