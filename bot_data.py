from pymongo import MongoClient
from dotenv import load_dotenv
import os
import _api
import pandas as pd
from tqdm import tqdm

load_dotenv()

client = MongoClient(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")),
                     username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"), authSource=os.getenv("DB_AUTH_DB"))
db = client[os.getenv("DB_AUTH_DB")]
collection = db[os.getenv("COL")]

def get_user_label():
    userDict={}
    file = open('../botometer-feedback-2019.tsv','r')
    for line in file:
        parts = line.split('\t')
        userDict[parts[0]]=parts[1].strip('\n')
    print (len(userDict))
    return userDict

def get_timeline_of_userid(ids,numcount,userDict):
    for i in tqdm(ids):
        try:
            for page in range(1,numcount):
                timeline = _api.get_api().user_timeline(user_id=i,count=200, tweet_mode="extended", wait_on_rate_limit=True,page=page)
                for t in timeline:
                    t = t._json
                    t['label'] = userDict[i]
                    collection.insert_one(t)
        except Exception as e:
            print (e)



# udict = get_user_label()
# get_timeline_of_userid(udict.keys(),2,udict)