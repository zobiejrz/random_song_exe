##################################################
#                                                #
#             random_song_exe v0.1               #
#             made by Ben Zobrist                #
#             © Ben Zobrist 2019                 #
#                                                #
##################################################

from datetime import datetime # IMPORTANT
from datetime import time # IMPORTANT
from datetime import timedelta # IMPORTANT
import time as t
import os # IMPORTANT
import json # IMPORTANT
import threading # IMPORTANT
import requests # IMPORTANT
from Song import *
from Album import *
import random
import base64 # IMPORTANT
import tweepy



def GetClientCredentials(spotify_client, spotify_secret):
    """Gets the Spotify Client credentials needed to perform api calls"""
    s = "{}:{}".format(spotify_client, spotify_secret)
    b = s.encode("UTF-8")
    e = base64.b64encode(b)

    header = {"Authorization": "Basic {}".format(e)}
    data = {'grant_type' : "client_credentials"}

    url = "https://accounts.spotify.com/api/token"
    a = requests.post(url, data=data, auth = (spotify_client, spotify_secret))

    creds = a.json()
    return creds['access_token']

def GetRandomSong(sc, ss):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(THIS_FOLDER, "wotd.json")
    wotd = {}
    with open(dir) as d:
        wotd = json.load(d)

    url = "https://api.spotify.com/v1/search?q={}&type=track&offset={}&limit=1".format(wotd["wotd"], random.randint(0, 10000))
    header = {"Authorization": "Bearer {}".format(GetClientCredentials(sc, ss))}
    a = requests.get(url, headers=header)

    # dir = os.path.join(THIS_FOLDER, "output.json")
    # with open(dir, "w") as d:
    #     json.dump(a.json(), d)

    item = a.json()["tracks"]["items"][0]

    artist = item["album"]["artists"][0]["name"]
    name = item["name"]
    link = item["external_urls"]["spotify"]

    newSong = Song(name, artist, link)
    return newSong

def SendTweet(input):
    try:
        api.update_status(input)
    except tweepy.TweepError as e:
        print(e.message)
    return

def Random_Song_Exe(sc, ss):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(THIS_FOLDER, "data.json")
    while True:
        data = {}
        with open(dir) as d:
            data = json.load(d)

        # These are getting updated every single loop in case the user decides to update them
        TIME_BETWEEN_UPDATES = timedelta(hours=data['timedelta']['hours'], minutes=data['timedelta']['minutes'], seconds=data['timedelta']['seconds']) # Time between each tweet
        time_of_last_tweet = datetime(year=data['lastTweet']['years'], month=data['lastTweet']['months'], day=data['lastTweet']['days'], hour=data['lastTweet']['hours'], minute=data['lastTweet']['minutes'], second=data['lastTweet']['seconds'])

        current_time = datetime.utcnow()

        currentTD = current_time - time_of_last_tweet
        if currentTD > TIME_BETWEEN_UPDATES:
            # Get Song Data
            song = GetRandomSong(sc, ss)
            # Tweet

            SendTweet(str(song))

            time_of_last_tweet = datetime.utcnow()
            data['lastTweet'] = {"years": time_of_last_tweet.year, "months": time_of_last_tweet.month, "days": time_of_last_tweet.day, "hours": time_of_last_tweet.hour, "minutes": time_of_last_tweet.minute, "seconds": time_of_last_tweet.second}
            with open(dir, "w") as d:
                json.dump(data, d)


# Pull in the data from the last time the bot was active
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

could_connect_to_spotify = True # In the future, random_song_exe will actually check if it can connect
could_connect_to_twitter = True # Now, the connection is assumed

print("##################################################\n" +
      "#                                                #\n" +
      "#             random_song_exe v0.1               #\n" +
      "#             made by Ben Zobrist                #\n" +
      "#             © Ben Zobrist 2019                 #\n" +
      "#                                                #\n" +
      "##################################################")

# Get keys from auth.json
auth_file = os.path.join(THIS_FOLDER, "auth.json")
auth = {}
with open(auth_file) as a:
    auth = json.load(a)

# Connect to Spotify

spotify_client = auth['spotify_client']
spotify_secret = auth['spotify_secret']

# Connect to Twitter

twitter_client = auth['twitter_client']
twitter_secret = auth['twitter_secret']
twitter_access_token = auth['twitter_access_token']
twitter_access_token_secret = auth['twitter_access_token_secret']

auth = tweepy.OAuthHandler(twitter_client, twitter_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# Ask whether to bootup if both connnections were successful

obtained_valid_input = False
should_start = ""
while obtained_valid_input == False:
    should_start = input("\nWould you like to start? [y/n]: ")
    if should_start == "y" or should_start == "n":
        obtained_valid_input = True
    else:
        print("I didn't quite get that, please type 'y' for yes, or 'n' for no.")

if should_start == "y":
    print("\n[ ACTIVE ]")
    print("Type 'quit' to turn off the bot. Push the enter key for other commands.\n")
    # Thread 1: Manage Tweets as expected -- Check delta times, etc...
    bot = threading.Thread(target=Random_Song_Exe, args=(spotify_client, spotify_secret,), daemon=True)
    bot.start()

    # Main Thread: User Input+Commands
    main_thread = threading.current_thread()
    user_input = ""
    while user_input != "quit":
        user_input = input(" >>> ")

        if user_input == "status":
            i = 0
            for t in threading.enumerate():
                if t == main_thread:
                        continue
                i+=1
            print("\nSTATUS")
            print("The bot is{} active.{}".format(" not" if i == 0 else "", " {} threads are active.".format(i) if i > 1 else ""))
            print("The last automated tweet was sent at {}.".format("datetime"))
            print("The next automated tweet will be sent at {}.\n".format("datetime"))

        elif user_input == "tweet":
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
                send_tweet = threading.Thread(target=SendTweet, args=(status_content,))
                send_tweet.start()
            else:
                print("Cancelled.\n")

        elif user_input != "quit":
            print("\nOPTIONS")
            print("%-10s" % "status " + "Prints the current status of the bot.")
            print("%-10s" % "tweet " + "Sends a tweet as the bot. Doesn't affect scheduling.")
            print("%-10s" % "quit " + "Turns the bot off.\n")
        else:
            print("[INACTIVE]")

print("\n\tGoodbye!\n")
