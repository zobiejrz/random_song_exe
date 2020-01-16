import threading
import os
import datetime
from datetime import timedelta
import json
import tweepy
import logging
import time

class Bot:

    def __init__(self):
        logging.basicConfig(filename='../Log/bot.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        self.bot_thread = threading.Thread()
        self.botShouldRun = False

    def Random_Song_Exe(self, api, spotify):
        """
        This is the bot function. Anything in here the bot does.
        """
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(THIS_FOLDER, "../Persistent/data.json")
        time_of_last_tweet = api.user_timeline(
            id=api.me().screen_name, count=1)[0].created_at
        while True:
            if not self.botShouldRun:
                break

            data = {}
            with open(dir) as d:
                data = json.load(d)

            # These are getting declared every single loop so the user can update them
            TIME_BETWEEN_UPDATES = timedelta(hours=data['timedelta']['hours'], minutes=data['timedelta']['minutes'], seconds=data['timedelta']['seconds']) # Time between each tweet

            current_time = datetime.datetime.utcnow()

            currentTD = current_time - time_of_last_tweet

            if currentTD > TIME_BETWEEN_UPDATES:
                tries = 0
                while True:
                  if tries == 3:
                      logging.critical("It 3 tries to make a tweet, it looks like someone made a fucky wucky :-(")
                      break
                  try:
                      # Get Song Data
                      song = spotify.GetRandomSong()
                      # Tweet
                      api.update_status(str(song))
                      time_of_last_tweet = api.user_timeline(
                          id=api.me().screen_name, count=1)[0].created_at
                      logging.debug('Tweet successful')
                  except Exception as e:
                      tries += 1
                      logging.critical(str(e))
                      logging.critical('A Critical Error occured while making a tweet.')

    def Toggle(self, api, spotify):
        """
        Toggle Bot On/Off
        """
        if self.bot_thread.isAlive():
            self.botShouldRun = False
            print("[INACTIVE]")
            print("Bot Terminated\n")
            self.bot_thread.join()
        else:
            self.botShouldRun = True
            self.bot_thread = threading.Thread(target=self.Random_Song_Exe, args=(api, spotify,), daemon=True)
            self.bot_thread.start()
            print("[ ACTIVE ]")
            print("Bot Activated\n")

    def IsRunning(self):
        return self.botShouldRun
