from .Bots import Bots 
from google import genai
from dotenv import load_dotenv
import os
import sys
from .prompts import system_prompt,news_report_prompt,react_to_reply_prompt,system_prompt_w_out_tweets
import json
from datetime import datetime, timezone,timedelta
import random
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler

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

LLM_MODEL = "gemini-2.5-pro-preview-06-05"
load_dotenv()

def trigger_react(bot_name,bot_id:int,fina_prompt:str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    db = Database()
    logging.info(f"trigger_react called with {bot_name}, {bot_id}")

    try:
        logging.info("Calling Gemini with model gemini-2.5-flash-preview-05-20")
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=fina_prompt,
        )
        logging.info("Gemini response received.")
    except Exception as e:
        logging.error(f"Failed to call Gemini: {e}")
    
    try:
        conn = db.get_connection()
        if conn is None:
            logging.exception("Failed to connect to database")
            return
        
        cur = conn.cursor()

    
        response = response.text

        logging.info(f"Response from Gemini: for bot {bot_name}")
        # Parse response
        curly_1 = response.find("{")
        curly_2 = response.rfind("}")
        if curly_1 != -1 and curly_2 != -1:
            response = response[curly_1:curly_2 + 1]

        logging.info(f"Response from bot {bot_name}:")
        bot_response_json = json.loads(response)
        #logging.info(f"Parsed JSON: {bot_response_json}")

        if bot_response_json.get("Istweet"):
            
            # randomize the time to add between 10 and 20 miunutes (can change)S
            seconds_to_add = random.uniform(10, 60*19)   
            #run_at = datetime.now(timezone.utc) + timedelta(hours=hours_to_add)
            run_at1 = datetime.now(timezone.utc) + timedelta(seconds=seconds_to_add)
            # add task to the database
            logging.info(f"Adding task for bot {bot_name} to tweet to run at {run_at1} with seconds to add {seconds_to_add}")

            cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Tweet",response,run_at1))
            conn.commit()

        elif bot_response_json.get("Islike"):

            # randomize the time to add between 1 and 4 hours (can change)
            seconds_to_add = random.uniform(10, 60*19)   

            logging.info(f"Adding task for bot {bot_name} to like")
            run_at2 = datetime.now(timezone.utc) + timedelta(seconds=seconds_to_add)
            logging.info(f"Adding task for bot {bot_name} to tweet to run at {run_at2} with seconds to add {seconds_to_add}")

            cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Like",response,run_at2))
            conn.commit()


        elif bot_response_json.get("Isdislike"):

            
            # randomize the time to add between 1 and 4 hours (can change)
            seconds_to_add = random.uniform(10, 60*19)   
            logging.info(f"Adding task for bot {bot_name} to dislike")
            run_at3 = datetime.now(timezone.utc) + timedelta(seconds=seconds_to_add)
            
            logging.info(f"Adding task for bot {bot_name} to tweet to run at {run_at3} with seconds to add {seconds_to_add}")

            cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Disike",response,run_at3))
            conn.commit()


        elif bot_response_json.get("Iscomment"):

            
            # randomize the time to add between 1 and 4 hours (can change)
            seconds_to_add = random.uniform(10, 60*17)   

            logging.info(f"Adding task for bot {bot_name} to comment")
            run_at4 = datetime.now(timezone.utc) + timedelta(seconds=seconds_to_add)

            
            logging.info(f"Adding task for bot {bot_name} to tweet to run at {run_at4} with seconds to add {seconds_to_add}")

            cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Comment",response,run_at4))
            conn.commit()

        else:
            # Do nothing
            pass
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        return
    finally:
        conn.close()



class BotsManager:
    def __init__(self, scheduler=None):
        self.bot_list = []

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.gemini_api_key )
        self.logger = logging.getLogger(__name__)
        self.newsBot = None
        self.db = Database()
        self.MIN_RANDOM_TIME = 1
        self.MAX_RANDOM_TIME = 4
        self.scheduler = scheduler or BackgroundScheduler()

    def create_bot(self, bot_name, bot_class, *args, **kwargs):
        
        if bot_name in self.bots:
            raise ValueError(f"A bot with the name '{bot_name}' already exists.")
        bot_instance = bot_class(*args, **kwargs)
        self.bots[bot_name] = bot_instance
        return bot_instance
    
    def get_bot_from_name(self, bot_name):
        
        for bot in self.bot_list:
            if bot.get_name() == bot_name:
                return bot
        return None
    
    def get_bot_from_id(self, bot_id):
    
        for bot in self.bot_list:
            if bot.get_id() == bot_id:
                return bot
        return None

    def load_bots(self,jsonFile):
        # Load data from a JSON file
        with open(jsonFile, 'r') as f:
            bots = json.load(f)

        for bot in bots:

            try:
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

                if (bot["username"] == "News"):
                    self.newsBot = Bots(bot["username"],bot["prompt"],bot["tweet_interval"],bot_id)
                    self.logger.info(f"FOUND news bot: {self.newsBot.get_name()} (ID: {self.newsBot.id})")
                else:
                # create bot obj
                    botObj = Bots(bot["username"],bot["prompt"],bot["tweet_interval"],bot_id)
                    self.bot_list.append(botObj)
            except Exception as e:
                self.logger.exception(f"Error loading bot {bot['username']}: {e}")
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()


    def add_bot(self,bot):
        self.bot_list.append(bot)

    
    def fetch_replies(self,target_tweet_id):
        
        string_of_tweets = ""
        
        try:
            conn = self.db.get_connection()

            if conn is None:
                self.logger.exception("Failed to connect to database")
                return
            
            cursor = conn.cursor()

            query = """
                SELECT tweets.id, tweets.text, users.username
                FROM tweets
                JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id =  %s;
            """

            cursor.execute(query, (target_tweet_id,))
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

    def samplefn(self):
        print("sample function called")
    # This function is when a specific bot wants to react to a specific tweet
    def react_to_replies(self,  target_tweet_id, bot):
        print("react to replies was called") 

        replies = self.fetch_replies(target_tweet_id)
        tweet = self.fetch_tweet(target_tweet_id)
        if not tweet:
            return
        if not replies:
            return
        
        bot_persionality = bot.get_prompt()
        fina_prompt = react_to_reply_prompt.format(personality=bot_persionality,tweet=tweet, reply=replies)
        response = self.client.models.generate_content(
            model=LLM_MODEL, contents=fina_prompt,)


        conn = self.db.get_connection()
        if conn is None:
            self.logger.exception("Failed to connect to database")
            return
        cur = conn.cursor() 

        response.replace("target_tweet_id", target_tweet_id)
        
        # randomize the time to add between 1 and 4 hours (can change)
        seconds_to_add = random.uniform(self.MIN_RANDOM_TIME, self.MAX_RANDOM_TIME)

        run_at = datetime.now(timezone.utc) + timedelta(seconds=seconds_to_add)

        cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot.get_id(),"Comment",response,run_at))
        # Parse response

        bot_response_json = json.loads(response)
        content = bot_response_json.get("content", "")
        if content:
            bot.comment(content, target_tweet_id)
    

    # This function is used to react to tweets, If you want to react to a specific tweet, you can pass content of the tweet
    # To react to all tweets, you can just pass an empty string
    def react_to_tweets(self, tweet_to_react=""):
    
        logging.info("react to tweets was called") 
        if tweet_to_react:
            # If a specific tweet is provided, react to that tweet
            final_promt  = f"The news bot has tweeted the news that {tweet_to_react}.\n"
            recent_tweets = self.fetch_recent_tweets()

            final_promt += f"Here are the recent tweets from other bots for you to make a relevent new or you could just post news about things not related {recent_tweets}:\n"


            for bot in self.bot_list:
                bot_persionality = bot.get_prompt()
                fina_prompt = system_prompt.format(personality=bot_persionality,tweets=final_promt)
                


                random_time = random.randint(1, 10)
                #self.scheduler.add_job(trigger_react,'date',run_date=datetime.now(timezone.utc) + timedelta(seconds=random_time),args=[bot.get_name(),bot.get_id(),fina_prompt])
                self.scheduler.add_job(trigger_react,'date',run_date=datetime.now(timezone.utc) + timedelta(seconds=random_time),args=[bot.get_name(),bot.get_id(),fina_prompt])

                #job = scheduler.enqueue_in(timedelta(seconds=10), self.samplefn, bot_name=bot.get_name(),bot_id=bot.get_id(), fina_prompt=fina_prompt)
                #logging.info(f"Job {job.id} scheduled to run in {random_time} seconds for bot {bot.get_name()}")

        else:
            logging.info("Reacting to all tweets...")
            all_tweets = self.fetch_tweet()
            
            if not all_tweets:
                logging.info("No tweets found to react to.")
                all_tweets = ""
                
            for bot in self.bot_list:
                bot_persionality = bot.get_prompt()

                your_tweets = self.fetch_tweet(bot.get_id())

                fina_prompt = system_prompt.format(personality=bot_persionality,tweets=all_tweets,your_tweets=your_tweets)
                
                #logging.info(f"Final prompt for bot {bot.get_name()}: {fina_prompt}")
                random_time = random.randint(1, 10)
                #self.scheduler.add_job(trigger_react,'date',run_date=datetime.now(timezone.utc) + timedelta(seconds=random_time),args=[bot.get_name(),bot.get_id(),fina_prompt])
                self.scheduler.add_job(trigger_react,'date',run_date=datetime.now(timezone.utc) + timedelta(seconds=random_time),args=[bot.get_name(),bot.get_id(),fina_prompt])
                #logging.info(f"promt for bot {bot.get_name()}: {fina_prompt}")
                #job = scheduler.enqueue_in(timedelta(seconds=10),self.samplefn, bot_name=bot.get_name(),bot_id = bot.get_id(), fina_prompt=fina_prompt)
                #logging.info(f"Job {job.id} scheduled to run in {random_time} seconds for bot {bot.get_name()}")
        
    def report_news(self):
        print("report_news was called")  
        logging.info("Reporting news...")
        all_tweets = self.fetch_recent_tweets()

        if not all_tweets:
            all_tweets = ""
        
        bot_persionality = self.newsBot.get_prompt()
        fina_prompt = news_report_prompt.format(personality=bot_persionality,tweets=all_tweets)
        
        #logging.info(f"Final prompt for news report: {fina_prompt}")
        
        response = self.client.models.generate_content(
            model=LLM_MODEL, contents=fina_prompt,)
        response = response.text

        logging.info(f"Response from Gemini: {response}")
        # Parse response
        curly_1 = response.find("{")
        curly_2 = response.rfind("}")
        if curly_1 != -1 and curly_2 != -1:
            response = response[curly_1:curly_2 + 1]

        bot_response_json = json.loads(response)
        res = bot_response_json.get("content", "")
        if res:
            self.newsBot.tweet(res)
        
        # calls on every bot to react to the news
        #self.react_to_tweets(self.newsBot,res)

    def fetch_recent_tweets(self):
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
                JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id IS NULL ORDER BY timestamp DESC LIMIT 1000;
            """

            query_for_comments ="""
                SELECT tweets.id, tweets.text, users.username
                FROM tweets
                JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id IS NOT NULL ORDER BY timestamp DESC LIMIT 20;
            """

            cursor.execute(query)
            results = cursor.fetchall()

            for tweet_id, text, username in results:
                comments_on_each_tweet = self.fetch_replies(tweet_id)
                one_tweet = f"""
                --- TWEET START ---
                User: @{username}
                Tweet ID: {tweet_id}
                Text: {text}
                Replies: {comments_on_each_tweet}
                --- TWEET END --- \n
                """

                string_of_tweets += one_tweet
            return (string_of_tweets)

        except Exception as e:
            self.logger.exception(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    def fetch_tweet(self,id=None):
        
        string_of_tweets = ""
    
            
        try:
            conn = self.db.get_connection()
        
            if conn is None:
                self.logger.exception("Failed to connect to database")
                return
            cursor = conn.cursor()
            if id:
                query = """
                    SELECT tweets.id, tweets.text, users.username
                    FROM tweets
                    JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id IS NULL AND tweets.id = %s;
                """

                
                query2 = """
                    SELECT tweets.id, tweets.text, users.username
                    FROM tweets
                    JOIN users ON tweets.author_id = users.id
                    WHERE tweets.parent_tweet_id IS NULL
                    ORDER BY tweets.timestamp DESC
                    id not in (%s)
                    LIMIT 1000;
                    
                """
                cursor.execute(query, (id,))
                results = cursor.fetchall()
            else:

                query = """
                    SELECT tweets.id, tweets.text, users.username
                    FROM tweets
                    JOIN users ON tweets.author_id = users.id
                    WHERE tweets.parent_tweet_id IS NULL
                    ORDER BY tweets.timestamp DESC
                    LIMIT 1000;
                    
                """

                fetch_comments_query = """
                    SELECT tweets.id, tweets.text, users.username
                    FROM tweets
                    JOIN users ON tweets.author_id = users.id WHERE tweets.parent_tweet_id IS NOT NULL;
                """

                cursor.execute(query)
                results = cursor.fetchall()

            for tweet_id, text, username in results:
                comments_on_each_tweet = self.fetch_replies(tweet_id)
                one_tweet = f"""
                --- TWEET START ---
                User: @{username}
                Tweet ID: {tweet_id}
                Text: {text}
                Replies: {comments_on_each_tweet}
                --- TWEET END --- \n
                """
                
                string_of_tweets += one_tweet

   
            return (string_of_tweets)

        except Exception as e:
            self.logger.exception(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

         
class BotDirector:
    def __init__(self):
        pass




def test():
    print("CWD:", os.getcwd())

    Batman = Bots("Batman","hello",2,233)

    bf = BotsManager()
    #bf.load_bots("character-config.json")
    bf.add_bot(Batman)


if __name__ == "__main__":
    bm = BotsManager()
    bm.load_bots("character-config.json")
    bm.react_to_tweets()

