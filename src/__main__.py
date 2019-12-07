##################################################
#                                                #
#             random_song_exe v0.1               #
#             made by Ben Zobrist                #
#             © Ben Zobrist 2019                 #
#                                                #
##################################################

from datetime import datetime
from datetime import time
from datetime import timedelta
import time as t
import os
import json
import threading
# import multiprocessing

def SendTweet(input):
    print(input)
    t.sleep(10)
    print("Finished tweeting.")
    return

def Random_Song_Exe(sc, ss, tc, ts, td, lt, dir):
    data_file = os.path.join(THIS_FOLDER, "data.json")

    while True:
        data = {}
        with open(dir) as d:
            data = json.load(d)

        # These are getting updated every single loop in case the user decides to update them
        TIME_BETWEEN_UPDATES = timedelta(days=data.timedelta['days'], hours=data.timedelta['hours'], minutes=data.timedelta['minutes'], seconds=data.timedelta['seconds']) # Time between each tweet
        time_of_last_tweet = timedate(data['lastTweet'])

        current_time = datetime.utcnow()

        currentTD = current_time - time_of_last_tweet
        print(dt5 >= TIME_BETWEEN_UPDATES)
        if currentTD > TIME_BETWEEN_UPDATES:
            # Get Song Data

            # Make Tweet

            # Tweet

            time_of_last_tweet = timedate.utcnow()
            data['lastTweet'] = time_of_last_tweet.strftime('%Y,%m,%d,%H,%M,%S')
            with open(dir) as d:
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
    bot = threading.Thread(target=Random_Song_Exe, daemon=True)
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
