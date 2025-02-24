import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify

from scrapers import walmartScraper
import datetime
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

if __name__ == '__main__':
    app.run(debug=True)