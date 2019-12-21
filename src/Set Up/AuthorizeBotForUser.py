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
"""

consumer_key = "xxx-xxx-123"
consumer_secret = "xxx-xxx-123"

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
