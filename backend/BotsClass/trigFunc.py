from .Bots import Bots 
from google import genai
from dotenv import load_dotenv
import os
import sys
from .prompts import system_prompt,news_report_prompt,react_to_reply_prompt
import json
from datetime import datetime, timezone,timedelta
import random
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler 
target_dir = os.path.join(os.getcwd(), "backend")
sys.path.append(target_dir)

from System.Database import Database

import logging


def trigger_react(bot_name,bot_id,fina_prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    db = Database()
    print(f"trigger_react called with {bot_name}, {bot_id}")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=fina_prompt,)

    conn = db.get_connection()
    if conn is None:
        logging.exception("Failed to connect to database")
        return
    cur = conn.cursor()
    response = response.text

    logging.info(f"Response from Gemini: {response} for bot {bot_name}")
    # Parse response
    curly_1 = response.find("{")
    curly_2 = response.rfind("}")
    if curly_1 != -1 and curly_2 != -1:
        response = response[curly_1:curly_2 + 1]

    logging.info(f"Response from bot {bot_name}: {response}")
    bot_response_json = json.loads(response)
    logging.info(f"Parsed JSON: {bot_response_json}")

    if bot_response_json.get("Istweet"):
        
        # randomize the time to add between 1 and 4 hours (can change)S
        hours_to_add = random.uniform(1, 4)

        run_at = datetime.now(timezone.utc) + timedelta(hours=hours_to_add)
        
        # add task to the database
        cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Tweet",response,run_at))
        conn.commit()

    elif bot_response_json.get("Islike"):

        # randomize the time to add between 1 and 4 hours (can change)
        hours_to_add = random.uniform(1, 4)


        run_at = datetime.now(timezone.utc) + timedelta(hours=hours_to_add)
        cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Like",response,run_at))
        conn.commit()


    elif bot_response_json.get("Isdislike"):

        
        # randomize the time to add between 1 and 4 hours (can change)
        hours_to_add = random.uniform(1, 4)


        run_at = datetime.now(timezone.utc) + timedelta(hours=hours_to_add)
        cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Disike",response,run_at))
        conn.commit()


    elif bot_response_json.get("Iscomment"):

        
        # randomize the time to add between 1 and 4 hours (can change)
        hours_to_add = random.uniform(1, 4)


        run_at = datetime.now(timezone.utc) + timedelta(hours=hours_to_add)
        cur.execute("INSERT INTO tasks (bot_id,function,payload,run_at) VALUES (%s,%s,%s,%s)", (bot_id,"Comment",response,run_at))
        conn.commit()

    else:
        # Do nothing
        pass

 