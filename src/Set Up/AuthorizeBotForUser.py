import webbrowser
import tweepy

"""
Taken from https://github.com/tweepy/examples/blob/master/oauth/getaccesstoken.py

While logged into a twitter account, run this script to authorize the app and get
the user key+secret. Put those into the auth.json file to run the bot.

Note: The key+secret only need to be obtained once for each user.

EDITS:
The original code isnt compatible with Python 3 and was edited to fix compatibility issues.
Line 28 was originally two prints that showed the Key and Secret seprately, but was broken.
Lines 18-28 were added to automatically grab the keys from auth.json
"""

# Pull in the data from the last time the bot was active
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Gets keys from auth.json
auth_file = os.path.join(THIS_FOLDER, "../Persistent/auth.json")
auth = {}
with open(auth_file) as a:
    auth = json.load(a)

consumer_key = auth['twitter_client']
consumer_secret = auth['twitter_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Open authorization URL in browser
webbrowser.open(auth.get_authorization_url())

# Ask user for verifier pin
pin = input('Verification pin number from twitter.com: ').strip()

# Get access token
token = auth.get_access_token(verifier=pin)

# Give user the access token
print ('Access token:')
print (token)
