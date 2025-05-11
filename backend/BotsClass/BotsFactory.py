from Bots import Bots 
from google import genai
from dotenv import load_dotenv
import os
import sys
from prompts import system_prompt
import json


target_dir = os.path.join(os.getcwd(), "backend")
sys.path.append(target_dir)

from System.Database import Database

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


load_dotenv()



class BotsFactory:
    def __init__(self):
        self.bot_list = []

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.gemini_api_key )
        self.logger = logging.getLogger(__name__)

        self.db = Database()

    def create_bot(self, bot_name, bot_class, *args, **kwargs):
        """
        Creates and initializes a bot instance.

        :param bot_name: Unique name for the bot.
        :param bot_class: The class of the bot to be instantiated.
        :param args: Positional arguments for the bot class.
        :param kwargs: Keyword arguments for the bot class.
        :return: The created bot instance.
        """
        if bot_name in self.bots:
            raise ValueError(f"A bot with the name '{bot_name}' already exists.")
        bot_instance = bot_class(*args, **kwargs)
        self.bots[bot_name] = bot_instance
        return bot_instance
    
    def load_bots(self,jsonFile):
        # Load data from a JSON file
        with open(jsonFile, 'r') as f:
            bots = json.load(f)

        for bot in bots:
            conn = self.db.get_connection()
            cur = conn.cursor()
            # Check if the bot already exists by username
            cur.execute("SELECT id FROM users WHERE username = %s", (bot['username'],))
            existing = cur.fetchone()

            if existing:
                bot_id = existing[0]
                cur.execute("""
                    UPDATE users
                    SET bio = %s,  profile_picture = %s
                    WHERE username = %s
                """, (bot['bio'], bot['pfpUrl'], bot['username']))    
                self.logger.info(f"Bot {bot['username']} already exists with ID {bot_id}")
            else:
                # Insert the new bot
                cur.execute("""
                    INSERT INTO users (username, bio, profile_picture,email)
                    VALUES (%s, %s, %s,%s)
                    RETURNING id;
                """, (bot['username'], bot['bio'], bot['pfpUrl']," "))
                
                bot_id = cur.fetchone()[0]
                self.logger.info(f"Inserted {bot['username']} with ID {bot_id}")
            conn.commit()
            # create bot obj
            botObj = Bots(bot["username"],bot["prompt"],bot["tweet_interval"],bot_id)
            self.bot_list.append(botObj)


    def add_bot(self,bot):
        self.bot_list.append(bot)

    def get_bot(self, bot_name):
        """
        Retrieves a bot instance by its name.

        :param bot_name: The name of the bot to retrieve.
        :return: The bot instance if found, otherwise None.
        """
        return self.bots.get(bot_name)

    def list_bots(self):
        """
        Lists all created bots.

        :return: A list of bot names.
        """
        return list(self.bots.keys())
    
    def react_to_tweets(self,bot):
        all_tweets = self.fetch_all_tweets()

        if not all_tweets:
            return
        
        bot_persionality = bot.get_prompt()
        fina_prompt = system_prompt.format(personality=bot_persionality,tweets=all_tweets)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=fina_prompt,)


        # Parse response

        bot_response_json = json.loads(response)

        if bot_response_json.get("Istweet") == True:
            pass

        if bot_response_json.get("Istweet"):
            tweet_data = bot_response_json.get("Tweet", {})
            tweet_content = tweet_data.get("contents", [])
            bot.tweet(tweet_content)

        elif bot_response_json.get("Islike"):
            like_data = bot_response_json.get("Like", {})
            tweet_ids = like_data.get("tweetIds", [])
            for tweet_id in tweet_ids:
                bot.like(tweet_id)

        elif bot_response_json.get("Isdislike"):
            dislike_data = bot_response_json.get("Dislike", {})
            tweet_ids = dislike_data.get("tweetIds", [])
            for tweet_id in tweet_ids:
                bot.dislike(tweet_id)

        elif bot_response_json.get("Iscomment"):
            comment_data = bot_response_json.get("Comment", {})
            comment_content = comment_data.get("content", "")
            post_id = comment_data.get("tweetId", "")
            bot.comment(comment_content, post_id)

        else:
            # Do nothing
            pass



    def fetch_all_tweets(self):
        
        string_of_tweets = ""
        conn = self.db.get_connection()
        
        if conn is None:
            self.logger.exception("Failed to connect to database")
            return
            
        try:

            cursor = conn.cursor()

            query = """
                SELECT tweets.id, tweets.text, users.username
                FROM tweets
                JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id IS NULL;
            """

            cursor.execute(query)
            results = cursor.fetchall()

            for tweet_id, text, username in results:
                one_tweet = f" {username} tweeted: {text} (tweet_id: {tweet_id})\n"
                string_of_tweets += one_tweet
            return (string_of_tweets)

        except Exception as e:
            self.logger.exception(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

         



def test():
    print("CWD:", os.getcwd())

    Batman = Bots("Batman","hello",2,233)

    bf = BotsFactory()
    bf.load_bots("character-config.json")

test()