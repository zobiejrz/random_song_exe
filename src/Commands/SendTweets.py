import threading
import os
import json
import datetime
import tweepy
from datetime import timedelta

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
bot_thread = threading.Thread()
botShouldRun = False

def Tweet(api, input):
    try:
        api.update_status(input)
    except tweepy.TweepError as e:
        print(e)

def SingleStatus(api):
    valid_length = False
    status_content = ""

    while not valid_length:

        print("\nType out your tweet. Leave the field blank to cancel.")
        status_content = input()

        if len(status_content) > 280:
            print("Tweets can only be up to 280 characters. Yours is {} characters.".format(len(status_content)))
        else:
            valid_length = True

    if len(status_content) != 0:
        send_tweet = threading.Thread(target=Tweet, args=(api, status_content,))
        send_tweet.start()
    else:
        print("Cancelled.\n")
