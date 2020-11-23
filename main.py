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
#Pagination
for tweet in tweepy.Cursor(api.home_timeline).items(100):
    print(f"{tweet.user.name} said: {tweet.text}")
#Create Tweet
api.update_status("Test tweet from Tweepy")

#Get User Info
user = api.get_user('lipstick_whit')
print("User details:")
print(user.name)
print(user.description)
print(user.location)
#See User's followers
print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)

#Follow User
api.create_friendship(user)

#Update Profile Description
api.update_profile(description="I like Python")

#Block a user
for block in api.blocks():
    print(block.name)

#Search 
for tweet in api.search(q="Python", lang="en", rpp=10):
    print(f"{tweet.user.name}:{tweet.text}")

#Find Trends
trends_result = api.trends_place(1)
for trend in trends_result[0]["trends"]:
    print(trend["name"])

#See if you were mentioned
tweets = api.mentions_timeline()
for tweet in tweets:
    tweet.favorite()
    tweet.user.follow()


#How to view a stream 
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

# Authenticate to Twitter
auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Django", "Tweepy"], languages=["en"]