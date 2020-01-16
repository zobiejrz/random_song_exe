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
    data_dir = os.path.join(THIS_FOLDER, "../Persistent/data.json")
    data = {}
    with open(data_dir) as d:
        data = json.load(d)

    days = data['timedelta']['days']
    hours = data['timedelta']['hours']
    minutes = data['timedelta']['minutes']
    seconds = data['timedelta']['seconds']
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    # print("{}:{}:{}:{}".format(days, hours, minutes, seconds))
    next_time = (GetTimeOfLastTweet(api) + delta)

    return next_time.strftime("%m/%d/%Y, %H:%M:%S")

def GetTimeOfLastTweet(api):
    tweet = api.user_timeline(id = api.me().screen_name, count = 1)[0]
    return tweet.created_at

def GetTotalNumberOfTweets(api):
    return api.me().statuses_count


def PrintStatus(api, random_song_exe):
    """
    Prints the bot status
    """
    print("\nSTATUS")
    print("%-25s" % "Is Active" + "{}".format("[ ACTIVE ]" if random_song_exe.IsRunning() else "[INACTIVE]"))
    print("%-25s" % "Number of Threads" + "{}".format(GetNumberOfThreads()))
    print("%-25s" % "Number of Tweets" + "{}".format(GetTotalNumberOfTweets(api)))
    print()
    print("%-25s" % "Frequency of Tweets" + "{}".format(GetFrequency()))
    print("%-25s" % "Time of Next Tweet" + "{} (Last tweet at {})".format(GetTimeToNextTweet(api), GetTimeOfLastTweet(api).strftime("%H:%M:%S")))
    print("%-25s" % "Current Time" + "{}".format(datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")))
    print()
