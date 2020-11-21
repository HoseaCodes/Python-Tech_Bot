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
user = api.me()
print(user)
search = ['#techintership', '#devintern', '#techcareers', '#techjobs', '#referme', '#breakintotech', '#techstartups', '#facebookcareers']
numTweet = 500

for items in search:
    items

for tweet in tweepy.Cursor(api.search, items).items(numTweet):
    try:
        print('Tweet Liked')
        tweet.favorite()
        print('Retweet done')
        tweet.retweet()
        time.sleep(50)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break