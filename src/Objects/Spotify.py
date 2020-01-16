##################################################
#                                                #
#             random_song_exe v0.1               #
#             made by Ben Zobrist                #
#             © Ben Zobrist 2019                 #
#                                                #
##################################################

import json
import requests
import os
from random import randint
import random
import base64
from Song import Song
import logging
import time

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Spotify:

    def __init__(self, client=0, secret=0):
        self.spotify_client = client
        self.spotify_secret = secret
        self.wordlist = open(THIS_FOLDER + "/../Persistent/wordlist.txt").readlines()
        logging.basicConfig(filename='../Log/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def GetClientCredentials(self):
        """
        Gets the Spotify Client credentials needed to perform api calls
        """

        # Make authorization code
        str = "{}:{}".format(self.spotify_client, self.spotify_secret)
        utf_str = str.encode("UTF-8")
        auth_code = base64.b64encode(utf_str)

        # Make the POST request
        header = {"Authorization": "Basic {}".format(auth_code)}
        data = {'grant_type' : "client_credentials"}
        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, data=data, auth = (self.spotify_client, self.spotify_secret))

        creds = response.json() # credential object

        return creds['access_token']

    def GetRandomSong(self):
        """
        Gets a random song by searching spotify using wotd and returning a random offset
        """
        # Get a word from the word list
        word = self.wordlist[random.randint(0, 99)]

        # Get the json from spotify
        tries = 0
        while True:
          try:

            if tries == 3:
              logging.critical('It took 3 tries to find a song, None was returned')
              return None

            query_url = "https://api.spotify.com/v1/search?q={}&type=track&offset={}&limit=1".format(word, random.randint(0, 250))
            header = {"Authorization": "Bearer {}".format(self.GetClientCredentials())}
            response = requests.get(query_url, headers=header)
            item = response.json()["tracks"]["items"][0]
            break
          except:
            logging.error('There was an Error getting a song with the word {}'.format(word))
            tries += 1
            time.sleep(10) # We are not trying to look like a DDOS attack

        # Parse variables
        artist = item["album"]["artists"][0]["name"]
        name = item["name"]
        link = item["external_urls"]["spotify"]

        # Make a song object+return
        newSong = Song(name, artist, link)
        return newSong