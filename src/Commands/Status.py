import threading
import os
import json
from datetime import *
from SendTweets import *
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def GetNumberOfThreads():
    """
    Gets the number of active threads
    """
    i = 0
    for t in threading.enumerate():
        i+=1
    return i

def GetWOTD():
    """
    Returns WOTD
    """
    word = {}
    wotd_dir = os.path.join(THIS_FOLDER, "../Persistent/wotd.json")
    with open(wotd_dir) as d:
        word = json.load(d)
    return word['wotd']

def GetFrequency():
    data_dir = os.path.join(THIS_FOLDER, "../Persistent/data.json")
    data = {}
    with open(data_dir) as d:
        data = json.load(d)

    days = data['timedelta']['days']
    hours = data['timedelta']['hours']
    minutes = data['timedelta']['minutes']
    seconds = data['timedelta']['seconds']
    return "{} day(s), {} hour(s), {} minute(s), {} second(s)".format(int(days), int(hours), int(minutes), int(seconds))

def GetTimeToNextTweet(api):
    tweet = api.user_timeline(id = api.me().screen_name, count = 1)[0]

    data_dir = os.path.join(THIS_FOLDER, "../Persistent/data.json")
    data = {}
    with open(data_dir) as d:
        data = json.load(d)

    days = data['timedelta']['days']
    hours = data['timedelta']['hours']
    minutes = data['timedelta']['minutes']
    seconds = data['timedelta']['seconds']
    delta = timedelta(days, hours, minutes, seconds)

    next_time = (tweet.created_at + delta)

    return next_time.strftime("%m/%d/%Y, %H:%M:%S")

def PrintStatus(api):
    """
    Prints the bot status
    """
    print("\nSTATUS")
    print("%-25s" % "Is Active" + "{}".format("[ ACTIVE ]" if bot_thread.isAlive() else "[INACTIVE]"))
    print("%-25s" % "Number of Threads" + "{}".format(GetNumberOfThreads()))
    print("%-25s" % "Current Word" + "{}".format(GetWOTD()))
    print("%-25s" % "Frequency of Tweets" + "{}".format(GetFrequency()))
    print("%-25s" % "Time of Next Tweet" + "{}".format(GetTimeToNextTweet(api)))
    print()
