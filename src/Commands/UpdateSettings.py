import os
import json
import threading
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def PrintOptions():
    """
    Prints all commands
    """
    print("\nOPTIONS")
    print("%-10s" % "status" + "Prints the current status of the bot.")
    print("%-10s" % "wotd" + "Change the word used to search for songs.")
    print("%-10s" % "freq" + "Change the frequency of tweets.")
    print("%-10s" % "toggle" + "Turns the bot on/off")
    print("%-10s" % "tweet" + "Sends a tweet as the bot. Doesn't affect scheduling.")
    print("%-10s" % "options" + "Display options.")
    print("%-10s" % "quit" + "Turns the bot off.\n")

def UpdateWOTD():
    """
    Gets user input to change the WOTD
    """
    new_word = input("What is the new word/phrase: ")
    word_json = {'wotd': '{}'.format(new_word)}

    wotd_dir = os.path.join(THIS_FOLDER, "../Persistent/wotd.json")
    with open(wotd_dir, "w") as d:
        json.dump(word_json, d)

    print("'{}' is now the new word\n".format(new_word))

def UpdateFreq():
    """
    Gets user input to update the frequency of tweets
    """

    data_dir = os.path.join(THIS_FOLDER, "../Persistent/data.json")

    # Get times + make sure they are positive integers
    # Also ensure they are not all zero
    while True:
        print("Please indicate how much time should occur between tweets:")
        new_days = GetPositiveInteger("Days")
        new_hours = GetPositiveInteger("Hours")
        new_minutes = GetPositiveInteger("Minutes")
        new_seconds = GetPositiveInteger("Seconds")

        if (new_days == 0 and new_hours == 0 and new_minutes == 0 and new_seconds == 0):
            print("The new values can't all be zero.\n")
        else:
            break

    # Get the whole json data object so we don't lose the time of the last tweet
    data = {}
    with open(data_dir) as d:
        data = json.load(d)

    data['timedelta']['days'] = new_days
    data['timedelta']['hours'] = new_hours
    data['timedelta']['minutes'] = new_minutes
    data['timedelta']['seconds'] = new_seconds

    with open(data_dir, "w") as d:
        json.dump(data, d)

    # Retrieve timedelta again to ensure it was saved
    data = {}
    with open(data_dir) as d:
        data = json.load(d)

    days = data['timedelta']['days']
    hours = data['timedelta']['hours']
    minutes = data['timedelta']['minutes']
    seconds = data['timedelta']['seconds']

    print("Tweets will now occur every {} day(s), {} hour(s), {} minute(s), and {} second(s).\n".format(int(days), int(hours), int(minutes), int(seconds)))

def GetPositiveInteger(title):
    """
    Gets a postive integer from the user. Uses arguement as a prompt
    """
    while True:
        try:
            output_str = input("{}: ".format(title))
            output = float(output_str)

            if (output < 0 or not output.is_integer()):
                print("Input must be a positive integer")
            else:
                return output
        except ValueError:
            print("Input must be a positive integer")
