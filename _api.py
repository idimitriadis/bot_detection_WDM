import tweepy
from dotenv import load_dotenv
import os
load_dotenv()

def get_api():
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

