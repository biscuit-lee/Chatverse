
import requests
""" BOTS LOGIC
    BOTS TWEETS WHEN  someone @ to him
    BOTS tweets when someone he follows post thigns if he has any opinions on the post
    BOTS subscribe to the news
    BOTS can perfom these actions:
        - Like
        - Dislike
        - Comment
        - Tweet
        - Do nothing
        - (Follow) 
        
    should bots have memories?
""" 

import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),      # logs to a file
        logging.StreamHandler()              # also prints to terminal
    ]
)

class Bots:
    def __init__(self, name, prompt, tweet_interval,id):
        self.name = name
        self.prompt = prompt
        self.tweet_interval = tweet_interval
        self.id = id
        logging.info(f"Initialized bot: {self.name} (ID: {self.id})")


    def get_name(self):
        return self.name
    def get_prompt(self):
        return self.prompt
    def get_id(self):
        return self.id
    def follow(self,username):
        pass
    
    
    def like(self,tweetId:int):
        if not isinstance(tweetId, int):
            logging.error(f"{self.name} tried to like a tweet with an invalid ID: {tweetId}")
            return

        url = "http://localhost:5000/api/addlike"
        data = {
            "userId" : self.id,
            "tweetId" : tweetId
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                logging.info(f"{self.name} liked: Tweet with id {tweetId}")
            else:
                logging.warning(f"{self.name} failed to tweet. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while {self.name} tried tweeting: {e}")

    def dislike(self,tweetId: int):
        if not isinstance(tweetId, int):
            logging.error(f"{self.name} tried to dislike a tweet with an invalid ID: {tweetId}")
            return

        url = "http://localhost:5000/api/dislike"
        data = {
            "userId" : self.id,
            "tweetId" : tweetId
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                logging.info(f"{self.name} liked: Tweet with id {tweetId}")
            else:
                logging.warning(f"{self.name} failed to tweet. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while {self.name} tried tweeting: {e}")


    def tweet(self,content):
            url = "http://localhost:5000/api/tweets"
            data = {
                "userId" : self.id,
                "content" : content
            }

            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    logging.info(f"{self.name} tweeted: {content}")
                else:
                    logging.warning(f"{self.name} failed to tweet. Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error while {self.name} tried tweeting: {e}")


    def comment(self,content, parentTweetId):
        if not isinstance(parentTweetId, int):
            logging.error(f"{self.name} tried to comment with an invalid parent ID: {parentTweetId}")
            return
        url = "http://localhost:5000/api/2/handleComment"
        data = {
            "userId" : self.id,
            "content" : content,
            "tweetId": parentTweetId
        }

        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                logging.info(f"{self.name} Commented: {content} on post with ID {parentTweetId}")
            else:
                logging.warning(f"{self.name} failed to tweet. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while {self.name} tried tweeting: {e}")



