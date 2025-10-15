from datetime import datetime,timezone
import time
import logging
#from BotsManager import BotsManager
from backend.BotsClass.BotsManager import BotsManager
from System.Database import Database
import json    
from apscheduler.schedulers.background import BackgroundScheduler
import keyboard




def setup_bots(botmanager):
    # Initialize the database connection
    db = Database()
    conn = db.get_connection()
    if conn is None:
        logging.error("Failed to connect to database")
        return

    # Set up loggingz
    logging.basicConfig()


    botmanager.load_bots("character-config.json")  # Load bots from the database

# This function runs every x minutes and report a randomized/real news
def report_news(botmanager):
    botmanager.report_news()

# every x mintues, the bots check all the tweets and decide to do the following actions: tweet, like, dislike, comment or do nothing
def bots_periodic_react(botmanager):
    
    #botmanager.load_bots("character-config.json")  # Load bots from the database    

    botmanager.react_to_tweets()

# This function runs every x minutes and check if there are any tasks to run
def check_for_tasks_to_run(botmanager):
    db = Database()
    conn = db.get_connection()
    # Set up logging
    logging.basicConfig()    

    if conn is None:
        logging.error("Failed to connect to database")
        return
    

    logging.info("Checking for tasks to run...")
    cursor = conn.cursor()
    # Fetch tasks from the database
    cursor.execute("SELECT * FROM tasks WHERE status = 'pending'")
    tasks = cursor.fetchall()
    if tasks:
        logging.info(f"Found {len(tasks)} tasks to process.")
        for task in tasks:
            task_id = task[0]
            bot_id = task[1]
            task_type = task[2]
            payload = task[3]
            run_at = task[4]
            status = task[5]
            created_at = task[6]
            task_handled = False

            if run_at.tzinfo is None:
                run_at = run_at.replace(tzinfo=timezone.utc)
            
            logging.info(f"run_at: {run_at}, current time: {datetime.now(timezone.utc)}")
            # Check if the task is due to run
            if (datetime.now(timezone.utc) >= run_at):
                # Process the task
                logging.info(f"Processing task {task_id} of type {task_type}")

                # Parse response

                bot_response_json = json.loads(payload)
                bot = botmanager.get_bot_from_id(bot_id)
                if bot is None:
                    logging.error(f"Bot with ID {bot_id} not found.")
                    continue
                

                if bot_response_json.get("Tweet"):
                    
                    task_handled = True
                    
                    tweet_data = bot_response_json.get("Tweet", {})
                    
                    tweet_content = tweet_data.get("contents", [])
                    
                    for each_tweet in tweet_content:
                        logging.info(f"{bot.get_name()} is tweeting with payload (after): {each_tweet}")
                        bot.tweet(each_tweet)

                if bot_response_json.get("Like"):
                    logging.info(f"{bot.get_name()} like tweets...")
                    task_handled = True
                    like_data = bot_response_json.get("Like", {})
                    tweet_ids = like_data.get("tweetIds", [])
                    for tweet_id in tweet_ids:
                        # Ensure tweet_id is an integer
                        try:
                            if isinstance(tweet_id, str):
                                tweet_id = int(tweet_id)
                            elif not isinstance(tweet_id, int):
                                raise ValueError(f"Invalid tweet_id type: {type(tweet_id)}")
                        
                        except ValueError as e:
                            logging.error(f"Error processing tweet_id {tweet_id}: {e}")
                            continue
                        bot.like(tweet_id)

                if bot_response_json.get("Dislike"):
                    logging.info(f"{bot.get_name()} dislike tweets...")
                    task_handled = True
                    dislike_data = bot_response_json.get("Dislike", {})
                    tweet_ids = dislike_data.get("tweetIds", [])
                    for tweet_id in tweet_ids:
                        # Ensure tweet_id is an integer
                        try:
                            if isinstance(tweet_id, str):
                                tweet_id = int(tweet_id)
                            elif not isinstance(tweet_id, int):
                                logging.error(f"Invalid tweet_id type: {type(tweet_id)}")
                                raise ValueError(f"Invalid tweet_id type: {type(tweet_id)}")
                        
                        except ValueError as e:
                            logging.error(f"Error processing tweet_id {tweet_id}: {e}")
                            continue
                        logging.info(f"{bot.get_name()} is disliking tweet with ID: {tweet_id}")
                        bot.dislike(tweet_id)

                if bot_response_json.get("Comment"):
                    #logging.info(f"{bot.get_name()} Comment tweets...")
                    task_handled = True
                    comment_data = bot_response_json.get("Comment", {})

                    id_lists = comment_data.get("tweetId", [])
                    content_lists = comment_data.get("content", [])

                    logging.info(f"{bot.get_name()} is commenting on tweets with IDs: {id_lists} and contents: {content_lists}")
                    """ comment_content = comment_data.get("content", "")
                    post_id = comment_data.get("tweetId", "")
                    """
                    #logging.info(f"Comment content: {comment_content}, Post ID: {post_id}")
                    
                    for i in range(len(id_lists)):
                        try:
                            post_id = int(id_lists[i])

                        except ValueError as e:
                            logging.error(f"Error processing post_id {id_lists[i]}: {e}")
                            continue
                        content = content_lists[i]
                        #logging.info(f"{bot.get_name()} is commenting on post {post_id} with content: {comment_content}")
                        bot.comment(content, post_id)

                if task_handled:
                    # Update the task status to 'completed'
                    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = %s", (task_id,))
                    conn.commit()
                    
                else:
                    # Do nothing
                    continue
                    

                
    else:
        logging.info("No tasks to process.")

if __name__ == "__main__":


    scheduler2 = BackgroundScheduler()
    bots_manager = BotsManager(scheduler2)


    setup_bots(bots_manager)

    PERIODIC_REACT_INTERVAL = 60 * 12
    PERIODIC_NEWS_REPORT_INTERVAL = 60 * 21

    # periodic react to tweets
    scheduler2.add_job(bots_periodic_react, 'interval', seconds=PERIODIC_REACT_INTERVAL, id='bots_periodic_react_job',args=[bots_manager])

    # News reporter 
    scheduler2.add_job(report_news, 'interval', seconds=PERIODIC_NEWS_REPORT_INTERVAL, id='report_news_job',args=[bots_manager])

    # Should run every minutes
    scheduler2.add_job(check_for_tasks_to_run, 'interval', seconds=60, id='check_for_tasks_to_run_job',args=[bots_manager])

    scheduler2.start()
    print("Scheduler started. Waiting for jobs...")
    try:
        while True:
            time.sleep(1)

        """             # if press key S stop running
            if keyboard.is_pressed('s'):
                scheduler2.remove_job('bots_periodic_react_job')
                scheduler2.remove_job('report_news_job')
            if keyboard.is_pressed('q'):
                scheduler2.shutdown()
                print("Scheduler stopped.")
                 """

    except (KeyboardInterrupt, SystemExit):
        bots_manager.scheduler.shutdown()
