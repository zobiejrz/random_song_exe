##################################################
#                                                #
#             random_song_exe v0.1               #
#             made by Ben Zobrist                #
#             © Ben Zobrist 2019                 #
#                                                #
##################################################

from datetime import *
import os
import json
import threading
import requests
import tweepy
sys.path.insert(1, './Objects/')
from Spotify import *
sys.path.insert(1, './Commands/')
from CommandHandler import *

# Pull in the data from the last time the bot was active
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Get keys from auth.json
auth_file = os.path.join(THIS_FOLDER, "./Persistent/auth.json")
auth = {}
with open(auth_file) as a:
    auth = json.load(a)

# Get all the keys+credentials
spotify_client = auth['spotify_client']
spotify_secret = auth['spotify_secret']
twitter_client = auth['twitter_client']
twitter_secret = auth['twitter_secret']
twitter_access_token = auth['twitter_access_token']
twitter_access_token_secret = auth['twitter_access_token_secret']

# Set up Tweepy
auth = tweepy.OAuthHandler(twitter_client, twitter_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# Set up spotify
spotify = Spotify(spotify_client, spotify_secret)

# Set up bot threads
main_thread = threading.current_thread()

print("##################################################\n" +
      "#                                                #\n" +
      "#             random_song_exe v1.0               #\n" +
      "#             made by Ben Zobrist                #\n" +
      "#             © Ben Zobrist 2019                 #\n" +
      "#                                                #\n" +
      "##################################################")
print( "\nType 'options' to see available commands. Type 'quit' to close the program\n" )

# Begin CLI
TakeCommands(api, spotify)

print( "\n\tGoodbye!\n" )
