import json
import tweepy
import time
from datetime import datetime, timedelta, timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import smtplib
from email.mime.text import MIMEText
import config
from collections import deque

class RateLimiter:
    def __init__(self, requests_per_minute):
        self.requests_per_minute = requests_per_minute
        self.timestamps = deque(maxlen=requests_per_minute)

    def wait(self):
        """Wait if necessary to respect rate limits."""
        now = time.time()
        
        while self.timestamps and now - self.timestamps[0] > 60:
            self.timestamps.popleft()
        
        if len(self.timestamps) >= self.requests_per_minute:
            sleep_time = 61 - (now - self.timestamps[0])
            if sleep_time > 0:
                print(f"Rate limit reached, waiting {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
        
        self.timestamps.append(now)

# Create rate limiter instance
sheets_limiter = RateLimiter(requests_per_minute=60)

# Initialize Twitter client
client = tweepy.Client(
    bearer_token=config.BEARER_TOKEN,
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    access_token=config.ACCESS_KEY,
    access_token_secret=config.ACCESS_SECRET,
    wait_on_rate_limit=True
)

# Test configuration - single search term and minimal tweets
search_terms = ["#techjobs", '#breakintotech', '#BackendEngineer', 
'#startupjob', '#JobOpening', '#HiringNow', '#RemoteJob', '#RemoteWork',
'#itjobsfromhome', '#devjobs', '#LATech']  # Only one search term
num_tweets = 10  # Only fetch one tweet

# Google Sheets setup
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account_credentials.json", scope)
sheets_client = gspread.authorize(creds)
sheet = sheets_client.open("TechJobs").sheet1

# Email and SMS setup
SMTP_SERVER = config.SMTP_SERVER
SMTP_PORT = config.SMTP_PORT
EMAIL_ADDRESS = config.EMAIL_ADDRESS
EMAIL_PASSWORD = config.EMAIL_PASSWORD
RECIPIENT_EMAIL = config.RECIPIENT_EMAIL
BREVO_API_KEY = config.BREVO_API_KEY
BREVO_SMS_SENDER = config.BREVO_SMS_SENDER
BREVO_SMS_RECIPIENT = config.BREVO_SMS_RECIPIENT

def get_valid_start_time():
    """Get a valid start time that's within Twitter's allowed window."""
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=1)  # Only look back 1 day for testing
    return start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def map_tweet_to_row(tweet):
    """Extract relevant information from a tweet and format it into a row."""
    try:
        text = tweet.text
        hashtags = ", ".join([f"#{tag}" for tag in text.split() if tag.startswith("#")])
        links = ", ".join([word for word in text.split() if word.startswith("http")])
        title = text.split("\n")[0]  # Use the first line as the title
        company = "N/A"  # Placeholder (can be parsed from tweet text if available)
        location = "N/A"  # Placeholder (requires location parsing or tweet geo metadata)
        date_pulled = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        return [title, company, links, location, date_pulled, "No", "No", hashtags]
    except Exception as e:
        print(f"Error mapping tweet: {e}")
        return None

def save_to_sheet(data):
    """Save data to sheet without batching for testing."""
    if not data:
        print("No data to save")
        return

    try:
        sheets_limiter.wait()
        sheet.append_rows(data)
        print(f"Successfully saved {len(data)} rows to sheet")
    except Exception as e:
        print(f"Error saving to sheet: {e}")

def search_twitter_jobs():
    """Test version of Twitter job search with minimal API calls."""
    print("\n=== Running Test Version ===")
    job_data = []
    start_time = get_valid_start_time()
    
    print(f"Starting search from {start_time}")
    print(f"Searching for: {search_terms[0]}")
    print(f"Number of tweets to fetch: {num_tweets}")

    try:
        # Single Twitter API request
        tweets = client.search_recent_tweets(
            query=f"{search_terms[7]} lang:en -is:retweet",
            max_results=num_tweets,
            # start_time=start_time,
            expansions="geo.place_id",
            place_fields="country_code",
            tweet_fields=["created_at", "text"]
        )
        
        if not tweets.data:
            print("No tweets found")
            return

        print(f"Received {len(tweets.data)} tweets")
        print(tweets.data)
        print(tweets.includes)
        print(tweets)

        for tweet in tweets.data:
            try: 
                row = map_tweet_to_row(tweet)
                if row:
                    job_data.append(row)
                    print(f"Tweet text: {tweet.text[:100]}...")  # Print first 100 chars of tweet
            except Exception as e:
                print(f"Error processing tweet: {e}")

        if job_data:
            save_to_sheet(job_data)
            print(f"Successfully processed {len(job_data)} tweets")
        else:
            print("No new tweets to save")

    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    try:
        # Search tweets and save to Google Sheets
        search_twitter_jobs()
    except tweepy.TooManyRequests:
        print("Rate limit hit. Sleeping...")
        time.sleep(900) 
    except KeyboardInterrupt:
        print("\nTest terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")