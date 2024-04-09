from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from webcrawler import ResearchHall
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webcrawler import CrawlerTools
import threading

import os

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
open_ai_key = os.getenv('GPT_API_KEY')
gpt_client = OpenAI(api_key=open_ai_key)
from dotenv import load_dotenv

import time
import json

from convex import ConvexClient

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

load_dotenv(".env.local")
load_dotenv()

mongo_uri = os.getenv("MONGO_CONNECTION")
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))
mongodb = mongo_client.brokerai
foodhall_collection = mongodb["foodhalls"]

try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

client = ConvexClient(os.getenv("NEXT_PUBLIC_CONVEX_URL"))

app = Flask(__name__)


@app.get("/crawler/new/<search_key>")
@cross_origin()
def start_new_crawl(search_key):
    def task(client, search_key: str): # looks like this is how nathan mutated convex data. 
        id = client.mutation("findings:createFoodHall", {
                             "name": search_key.title()})
        hall = ResearchHall.ResearchHall(client, foodhall_collection, id, search_key.title())
        hall.run_in_parallel()
        print(hall)
        print("Done!")

    threading.Thread(target=task, args=(client, search_key)).start()
    
    return "{ 'status': 'success' }"


def get_relevant_halls():
    """returns list of relevant halls"""
    options = Options()
    options.page_load_strategy = 'eager'

    # Initialize browser instances
    browser = webdriver.Chrome(options=options)
    new_food_hall_article_links = CrawlerTools.scrape_google_alert(browser=browser)
    browser.quit()

    res = CrawlerTools.determine_food_halls_in_parallel(new_food_hall_article_links)
    
    return {
        "relevant_halls": res
    }

@app.get("/crawler/new_halls_today")
@cross_origin()
def get_new_halls_today():
    """Reads from Google alerts and adds food halls to database"""
    hall_objects = get_relevant_halls()["relevant_halls"][:3]  # Limiting to 3 for the example

    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Create a future for each API call
        futures = [executor.submit(start_new_crawl, hall['food_hall_name']) for hall in hall_objects]

        # Optionally, wait for each to complete and handle their result
        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"Task completed with result: {result}")
            except Exception as e:
                print(f"Task generated an exception: {e}")

    # Check database for valid research 
    return jsonify({"status": "success"})

@app.route("/done")
def finish_page():
    # html
    return """
    <body style="width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; font-size: 50px; font-family: monospace">Done</body>
    
    """


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3333)
