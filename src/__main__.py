##################################################
#                                                #
#             random_song_exe v1.0               #
#             made by Ben Zobrist                #
#             © Ben Zobrist 2019                 #
#                                                #
##################################################

from datetime import datetime # To save+check deltatime
from datetime import time
from datetime import timedelta
import time as t

def StartBot():
    # Thread 1: Manage Tweets as expected -- Check delta times, etc...

    # Thread 2: Standby for user input/commands
    pass

TIME_BETWEEN_UPDATES = timedelta(days=0, hours=1.0, minutes=0, seconds=0) # Time between each tweet in hours
could_connect_to_spotify = True
could_connect_to_twitter = True

print("##################################################\n" +
      "#                                                #\n" +
      "#             random_song_exe v0.1               #\n" +
      "#             made by Ben Zobrist                #\n" +
      "#             © Ben Zobrist 2019                 #\n" +
      "#                                                #\n" +
      "##################################################")

# Connect to Spotify

# Connect to Twitter

# Ask whether to bootup if both connnections were successful

obtained_valid_input = False
while not obtained_valid_input:
    if could_connect_to_spotify and could_connect_to_twitter:
        should_start = input("\nWould you like to start? [y/n]: ")
        if (should_start is "y"):
            StartBot()
        elif (should_start is "n"):
            obtained_valid_input = True
        else:
            print("I didn't quite get that, please type 'y' for yes, or 'n' for no...")

print("\n\tGoodbye!\n")

# dt3 = datetime.utcnow()
# t.sleep(3)
# dt4 = datetime.utcnow()
#
# dt5 = dt4 - dt3
# print(dt5 >= TIME_BETWEEN_UPDATES)
