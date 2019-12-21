from UpdateSettings import *
from SendTweets import *
from Status import PrintStatus
import sys
sys.path.insert(1, './Objects/')
from Bot import Bot

def TakeCommands(api, spotify):
    """
    Gets a user command and executes it
    """
    random_song_exe = Bot()
    while True:
        user_input = input(" >>> ")

        if user_input == "status":
            PrintStatus(api, random_song_exe)
        elif user_input == "wotd":
            UpdateWOTD()
        elif user_input == "freq":
            UpdateFreq()
        elif user_input == "toggle":
            random_song_exe.Toggle(api, spotify)
        elif user_input == "tweet":
            SingleStatus(api)
        elif user_input == "options":
            PrintOptions()
        elif user_input == "quit":
            break;
        else:
            print( "\n'{}' isn't understood input. Type 'options' to see valid commands.\n".format(user_input) )
