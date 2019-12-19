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
from Song import *
import tweepy
from Spotify import Spotify
botShouldRun = False

def PrintOptions():
    print("\nOPTIONS")
    print("%-10s" % "status" + "Prints the current status of the bot.")
    print("%-10s" % "wotd" + "Change the word used to search for songs.")
    print("%-10s" % "freq" + "Change the frequency of tweets.")
    print("%-10s" % "toggle" + "Turns the bot on/off")
    print("%-10s" % "tweet" + "Sends a tweet as the bot. Doesn't affect scheduling.")
    print("%-10s" % "options" + "Display options.")
    print("%-10s" % "quit" + "Turns the bot off.\n")

def GetUTCTime():
    return "UTC: {}".format(datetime.utcnow())

def SendTweet(input):
    try:
        api.update_status(input)
    except tweepy.TweepError as e:
        print(e.message)

def Random_Song_Exe(sc, ss):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(THIS_FOLDER, "data.json")
    while True:
        if not botShouldRun:
            break;

        data = {}
        with open(dir) as d:
            data = json.load(d)

        # These are getting declared every single loop so the user can update them
        TIME_BETWEEN_UPDATES = timedelta(hours=data['timedelta']['hours'], minutes=data['timedelta']['minutes'], seconds=data['timedelta']['seconds']) # Time between each tweet
        time_of_last_tweet = datetime(year=data['lastTweet']['years'], month=data['lastTweet']['months'], day=data['lastTweet']['days'], hour=data['lastTweet']['hours'], minute=data['lastTweet']['minutes'], second=data['lastTweet']['seconds'])

        current_time = datetime.utcnow()

        currentTD = current_time - time_of_last_tweet
        if currentTD > TIME_BETWEEN_UPDATES:
            # Get Song Data
            song = spotify.GetRandomSong()
            # Tweet

            SendTweet(str(song))

            time_of_last_tweet = datetime.utcnow()
            data['lastTweet'] = {"years": time_of_last_tweet.year, "months": time_of_last_tweet.month, "days": time_of_last_tweet.day, "hours": time_of_last_tweet.hour, "minutes": time_of_last_tweet.minute, "seconds": time_of_last_tweet.second}
            with open(dir, "w") as d:
                json.dump(data, d)

# Pull in the data from the last time the bot was active
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Get keys from auth.json
auth_file = os.path.join(THIS_FOLDER, "auth.json")
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
bot = threading.Thread()
main_thread = threading.current_thread()

print("##################################################\n" +
      "#                                                #\n" +
      "#             random_song_exe v0.1               #\n" +
      "#             made by Ben Zobrist                #\n" +
      "#             © Ben Zobrist 2019                 #\n" +
      "#                                                #\n" +
      "##################################################")
print( "\n{}\n".format(GetUTCTime()) )
print( "Type 'options' to see available commands. Type 'quit' to close the program\n" )
# Begin CLI
running = True
while running:
    user_input = input(" >>> ")

    if user_input == "status":
        i = 0
        for t in threading.enumerate():
            i+=1

        word = {}
        wotd_dir = os.path.join(THIS_FOLDER, "wotd.json")
        with open(wotd_dir) as d:
            word = json.load(d)

        print("\nSTATUS")
        print("%-30s" % "Is Active" + "{}".format("[ ACTIVE ]" if bot.isAlive() else "[INACTIVE]"))
        print("%-30s" % "Number of Threads Active" + "{}".format(i))
        print("%-30s" % "Time of next tweet" + "{}".format('datetime'))
        print("%-30s" % "Frequency of tweets" + "{}".format('datetime'))
        print()
        print("%-30s" % "WOTD" + "{}".format(word['wotd']))
        print("%-30s" % "Number of Tweets" + "{}".format(api.me().statuses_count))
        print()

    elif user_input == "wotd":
        new_word = input("What is the new word/phrase: ")
        word_json = {'wotd': '{}'.format(new_word)}

        wotd_dir = os.path.join(THIS_FOLDER, "wotd.json")
        with open(wotd_dir, "w") as d:
            json.dump(word_json, d)

        print("'{}' is now the new word\n".format(new_word))

    elif user_input == "freq":
        # new_hour = input("  Hours: ")
        # new_minute = input("Minutes: ")
        # new_second = input("Seconds: ")
        #
        # timedelta = { 'hours': '{}'.format(new_hour), 'minutes': '{}'.format(new_minute), 'seconds': '{}'.format(new_second) }
        #
        # old_data = {}
        # last_tweet = {}
        # wotd_dir = os.path.join(THIS_FOLDER, "data.json")
        # with open(wotd_dir) as d:
        #     old_data = json.load(d)
        #
        # last_tweet = old_data['lastTweet']
        #
        # data = {'timedelta': timedelta, 'lastTweet': last_tweet.json()}
        #
        # freq_dir = os.path.join(THIS_FOLDER, "data.json")
        # with open(freq_dir, "w") as d:
        #     json.dump(data, d)
        #
        # print("Tweets will now occur every {}:{} {}\n".format(new_word))
        pass
    elif user_input == "toggle":
        if bot.isAlive():
            botShouldRun = False
            print ( "[INACTIVE]" )
            print ( "Bot Terminated\n" )
            bot.join()
        else:
            bot = threading.Thread(target=Random_Song_Exe, args=(spotify_client, spotify_secret,), daemon=True)
            botShouldRun = True
            print ( "[ ACTIVE ]" )
            print ( "Bot Activated\n" )
            bot.start()

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
    elif user_input == "options":
        PrintOptions()
    elif user_input == "quit":
        running = False
    else:
        print( "\n'{}' isn't understood input. Type 'options' to see valid commands.\n".format(user_input) )

print( "\n\tGoodbye!\n" )
