import tweepy
import time
import config

#Authenticate to Twitter
CONSUMER_KEY = config.CONSUMER_KEY # API Key
CONSUMER_SECRET = config.CONSUMER_SECRET # API Secret
ACESS_KEY = config.ACESS_KEY # API Token
ACESS_SECRET = config.ACESS_SECRET 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.get_user('lipstick_whit')
print(f'{user.screen_name} has {user.followers_count} followers.')
for friend in tweepy.Cursor(api.friends).items():
    # Process the friend here
    process_friend(friend)