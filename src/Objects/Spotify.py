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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Spotify:

    spotify_client = 0
    spotify_secret = 0

    def __init__(self, client=0, secret=0):
        self.spotify_client = client
        self.spotify_secret = secret

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

        # Get the wotd
        dir = os.path.join(THIS_FOLDER, "../Persistent/wotd.json")
        wotd = {} # The word that is used in the search
        with open(dir) as d:
            wotd = json.load(d)

        # Get the json from spotify
        query_url = "https://api.spotify.com/v1/search?q={}&type=track&offset={}&limit=1".format(wotd["wotd"], 1 ) #random.randint(0, 500))
        header = {"Authorization": "Bearer {}".format(self.GetClientCredentials())}
        response = requests.get(query_url, headers=header)
        item = response.json()["tracks"]["items"][0]

        # Parse variables
        artist = item["album"]["artists"][0]["name"]
        name = item["name"]
        link = item["external_urls"]["spotify"]

        # Make a song object+return
        newSong = Song(name, artist, link)
        return newSong


### FOR TESTING ###

# Gets spotify authentication keys
# auth_file = os.path.join(THIS_FOLDER, "../auth.json")
# auth = {}
# with open(auth_file) as a:
#     auth = json.load(a)
# spotify_client = auth['spotify_client']
# spotify_secret = auth['spotify_secret']
#
# # Make Spotify Object + GetCredentials
# spotify = Spotify(spotify_client, spotify_secret)
# print(spotify.GetClientCredentials())
