import tweepy
import time
import config
from tkinter import*

#Authenticate to Twitter
CONSUMER_KEY = config.CONSUMER_KEY # API Key
CONSUMER_SECRET = config.CONSUMER_SECRET # API Secret
ACESS_KEY = config.ACESS_KEY # API Token
ACESS_SECRET = config.ACESS_SECRET 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# user = api.get_user('lipstick_whit')
user = api.me()
print(f'{user.screen_name} has {user.followers_count} followers.')

for follower in tweepy.Cursor(api.followers).items():
    follower.follow()

root = Tk()
root.geometry('500x500')
root.resizable(0,0)
root.title("Tech_Bot")
root.config(bg = 'gray')

Label(root, text = 'Twitter', font='arial 20 bold', bg='lightgray').pack()
Label(root, text = 'Tech_Bot', font='arial 20 bold', bg='lightgray').pack()

label1 = Label( root, text="Search")
E1 = Entry(root, bd =5)

label2 = Label( root, text="Number of Tweets")
E2 = Entry(root, bd =5)

label3 = Label( root, text="Response")
E3 = Entry(root, bd =5)

label4 = Label( root, text="Reply?")
E4 = Entry(root, bd =5)

label5 = Label( root, text="Retweet?")
E5 = Entry(root, bd =5)

label6 = Label( root, text="Favorite?")
E6 = Entry(root, bd =5)

label7 = Label( root, text="Follow?")
E7 = Entry(root, bd =5)

def getE1():
    return E1.get()

def getE2():
    return E2.get()

def getE3():
    return E3.get()


def getE4():
    return E4.get()

def getE5():
    return E5.get()

def getE6():
    return E6.get()

def getE7():
    return E7.get()


def mainFunction():
    getE1()
    search = getE1()
    
    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)
    
    getE3()
    phrase = getE3()
    
    getE4()
    reply = getE4()
    
    getE5()
    retweet = getE5()
    
    getE6()
    favorite = getE6()

    getE7()
    follow = getE7()

    if reply == "yes":
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Reply
                print('\nTweet by: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.user.id))
                tweetId = tweet.user.id
                username = tweet.user.screen_name
                api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetId)
                print ("Replied with " + phrase)
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break


    if retweet == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Retweet
                tweet.retweet()
                print('Retweeted the tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if favorite == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Favorite
                tweet.favorite()
                print('Favorited the tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if follow == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Follow
                tweet.user.follow()
                print('Followed the user')
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break       
            
submit = Button(root, text ="Submit", command = mainFunction)
label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
label4.pack()
E4.pack()
label5.pack()
E5.pack()
label6.pack()
E6.pack()
label7.pack()
E7.pack()
submit.pack(side =BOTTOM)

root.mainloop()

    
