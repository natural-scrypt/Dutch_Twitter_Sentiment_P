# This portion is designed to run in Python
# This file mines data from Twitter through its API, translate the tweets into english via googletrans and appends all the data in a csv file
pip install googletrans==4.0.0-rc1
from googletrans import Translator

import pandas as pd
import time
import traceback
import tweepy
import datetime

api_key = "xxxxxxxx"
api_secret = "xxxxxx"
access_token = "xxxx-xxx"
access_secret = "xxxx"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


#Scrape Tweets
tweets, text_query = [], 'politiek  AND -filter:retweets'
query = "politiek AND -filter:retweets"
count = 200
given_date= 2022-7-29

try:
    for tweet in api.search_tweets(q=query, count=count, result_type='recent',
                           include_entities=True,):
        # print(f"Raw tweet: {tweet}")
        tweet_text_full, tweet_text_translated = "", ""

        status = api.get_status(id = tweet.id, tweet_mode="extended")
        try:
            tweet_text_full = status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            tweet_text_full = status.full_text

        try:
            tr = Translator()

            if tweet.lang and tweet.lang not in ['en', 'und']:

                #print(f"Raw tweet: {tweet_text_full}")

                if tweet.text:
                    translated = tr.translate(tweet_text_full)
                    if translated:
                        tweet_text = translated.__dict__()["text"]
            else:
                tweet_text = tweet_text_full
        except Exception as e:
            traceback.print_exc()
            pass

        tweets.append((tweet.created_at, tweet_text_full, tweet_text,
                       tweet.user.name,
                       tweet.user.location, tweet.user.followers_count, tweet.lang))

        df_tr = pd.DataFrame(tweets,
                             columns=['created_at', 'text_raw', 'text_en', 'name', 'location',
                                      'followers_count', 'lang'])

        df_tr.to_csv('Full_text_politics_60.csv')
        time.sleep(3)

    print("Completed.")

except BaseException as e:
    traceback.print_exc()


now = datetime.datetime.now()
print("Current date and time: ")
print(str(now))


# Much of this script was assembled using multiple other scripts and joining them here.
# Special thanks for  Yuliya-HV for helping me assemble this script
#https://github.com/Yuliya-HV
