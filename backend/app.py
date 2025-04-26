import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request

import datetime
from System.Database import Database

app = Flask(__name__)

tweets = [{"id":1,"text":"HELLO CHAT", "author_id":1,"timestamp":"2003", "likes":1, "comment_amount":0,"parent_id":None},
            {"id":2,"text":"GDAY CHAT", "author_id":2,"timestamp":"2010", "likes":21, "comment_amount":1,"parent_id":None}
            ]

        
db = Database()

@app.route('/api/tweets',methods=["GET","POST"])
def handle_tweets():
    if request.method == "GET":

        return jsonify(tweets)


    # This handles if a user wants to post a tweet
    if request.method == "POST":

        conn = db.get_connection()

        
        if conn is None:
            return jsonify({"message": "FAILED to connect to database"}),500
        

        current_time = datetime.datetime.now()
        data = request.get_json()
        userId = data["userId"]
        content = data["content"]

        if not userId or not content:
            return jsonify({"message" : "Post request fail"}),400
        
        query = "INSERT INTO tweets (text,author_id,timestamp,likes,comment_amount,parent_tweet_id) values (%s,%s,%s,%s,%s,%s)"
        try:
            curr = conn.cursor()
            curr.execute(query,(content,userId,current_time,0,0,None))
            conn.commit()

            return jsonify({"message": "Successfully added tweet to db"}),200


        except Exception as e:
            return jsonify({"message": "FAILED to post tweet"}),500



        finally:
            conn.close()          
    

@app.route('/api/data', methods=['GET'])
def get_data():

    # Fetch from db
    conn = db.get_connection()

    if conn is None:
        return jsonify({"message ": "Failed to connect to database"}),500

    try:
        curr = conn.cursor()
        curr.execute("SELECT tweets.*,users.username FROM tweets JOIN users ON tweets.author_id = users.id")
        
        res = curr.fetchall()

        colnames = [desc[0] for desc in curr.description]
        result = [dict(zip(colnames, row)) for row in res]

        #print(result)
        return jsonify(result),200



        
    except Exception as e:
        return jsonify({"message": e}),500
    
    finally:
        conn.close()

@app.route('/api/addlike',methods=["POST"])
def add_like():
    if request.method == "POST":
        conn = db.get_connection()

        if conn is None:
            return jsonify({"message :" "Failed to connect to database"},500)
        
        data = request.get_json()
        tweetid = data["tweetId"]
        userId = data["userId"]

        query_addlike = "UPDATE tweets SET likes = likes + 1 WHERE id = %s" 
        query_userLike = "INSERT into likes "
        try:
            curr = conn.cursor()
            curr.execute(query_addlike,(tweetid,))

            conn.commit()
            return jsonify({"message": "Successfully liked the tweet"}),200
        except Exception as e:
            return jsonify({"Message ": e}),500

@app.route("/api/users/<int:user_id>", methods=["GET","POST"])
def handle_userProfile(user_id):
    if (request.method == "GET"):
        print("USER : " + str(user_id) + " API FETCH CALLED ")
        conn = db.get_connection()
        
        query = "SELECT * FROM users WHERE id = %s"
        query_for_tweet = "SELECT * FROM tweets where author_id = %s"

        try:
            curr = conn.cursor()
            curr.execute(query, (user_id,))
            res = curr.fetchall()  # This returns a list of tuple (example. [(1, "John", "john@example.com"),(...)])
            

            colnames = [desc[0] for desc in curr.description]

            curr.execute(query_for_tweet,(user_id,))
            res2 = curr.fetchall()
            colnames_tweet= [desc[0] for desc in curr.description]

            user_data = [dict(zip(colnames, row)) for row in res]
            tweet_data = [dict(zip(colnames_tweet,row)) for row in res2]
            
            # add tweets to the user
            if user_data:
                user_data[0]["tweets"] = tweet_data

            print(user_data)

            return jsonify(user_data),200
        except Exception as e:
            return jsonify({"Message ": e}),500

@app.route("/api/<int:post_id>/handleComment",methods=["POST","GET"])
def handleComment(post_id):

    if (request.method == "POST"):

        conn = db.get_connection()
        data = request.get_json()
        comment = data["content"]
        user_id = data["userId"]
        tweet_id = data["tweetId"]
        
        query ="INSERT INTO comments (tweet_id,user_id, content, created_at, parent_comment_id, likes) VALUES (%s,%s,%s,%s,%s,%s)"
        try:
            curr = conn.cursor()
            curr.execute(query,(tweet_id,user_id,comment,datetime.datetime.now(),None,0))
            curr.commit()
            return jsonify({"Message": "Successfully added comment"}),200
        except Exception as e:
            return jsonify({"Message ": e}),500
    
    if(request.method == "GET"):

        conn = db.get_connection()
        query = "SELECT * FROM comments where tweet_id = %s"
        try:
            curr = conn.cursor()
            curr.execute(query,(post_id,))
            res = curr.fetchall()

            colnames = [desc[0] for desc in curr.description]
            result = [dict(zip(colnames, row)) for row in res]
            
            return jsonify(result),200
        
        except Exception as e:
            return jsonify({"Message": e}),500

@app.route("/api/follow",methods=["POST"])
def add_follower():
    conn = db.get_connection()
    data = requests.get_json()
    follower_id = data["follower_id"]
    following_id = data["following_id"]

    query = " INSERT INTO followings (following_id, follower_id) VALUES (%s,%s)"

    try:
        curr = conn.cursor()
        curr.execute(query,(following_id,follower_id))
        curr.commit()

        return jsonify({"message": "Successfully added follwer"}),200
    except Exception as e:
        return jsonify({"message " : e}),500

@app.route('/api/login',methods=["POST"])
def login_verify():
    if request.method == "POST":
        conn = db.get_connection()
        
        if conn is None:
            return jsonify({"message ": "FAILED to connect to database"}),500
        
        data = request.get_json()
        username = data['username']
        password = data['password']
        query = "SELECT * from users where username = 'john' AND passhash ='123' "
        try:
            curr = conn.cursor()
            curr.execute(query)
            res = curr.fetchone()
            if res:
                return jsonify({"message ": "Logged in successfully "}),200
            else:
                return jsonify({"message ": "Login failed , Cannot find user "}),401
                
            
        except Exception as e:
            
            return (jsonify({"message" : f"error during query {str(e)}"},500))

        finally:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)