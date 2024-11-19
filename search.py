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

# Initialize Twitter client with basic rate limiting
client = tweepy.Client(
    bearer_token=config.BEARER_TOKEN,
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    access_token=config.ACCESS_KEY,
    access_token_secret=config.ACCESS_SECRET,
    wait_on_rate_limit=True
)

# Define search terms and other variables
search_terms = ['#techstartups']
num_tweets = 5  # Reduced number of tweets per search

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

def handle_twitter_request(func, *args, **kwargs):
    """Wrapper function to handle Twitter API requests with retries."""
    max_retries = 3
    base_delay = 60  # Base delay in seconds
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except tweepy.TooManyRequests:
            if attempt == max_retries - 1:
                raise
            wait_time = base_delay * (attempt + 1)
            print(f"Rate limit reached. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Error: {e}. Retrying... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(base_delay)

def get_existing_urls(retries=3, delay=5):
    """Get existing URLs with retry mechanism."""
    for attempt in range(retries):
        try:
            sheets_limiter.wait()
            # Get all values and check if there's any data
            all_values = sheet.get_all_values()
            if len(all_values) <= 1:  # Only header row or empty
                print("Sheet is empty or contains only headers")
                return set()
            
            # Get URL column (index 2 for 3rd column)
            urls = [row[2] for row in all_values[1:] if len(row) > 2]  # Skip header row
            print(f"Successfully read {len(urls)} URLs from sheet")
            return set(urls)
        except Exception as e:
            if attempt == retries - 1:
                print(f"Final attempt failed: {e}")
                return set()  # Return empty set as fallback
            print(f"Error fetching URLs (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    return set()

def get_valid_start_time():
    """Get a valid start time that's within Twitter's allowed window."""
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=5)  # Reduced to 5 days to be safe
    return start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def send_notifications(message):
    """Send both email and SMS notifications with error handling."""
    try:
        send_email("Google Sheet Updated", message)
        print("Email notification sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

    try:
        send_sms(message)
        print("SMS notification sent successfully")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def save_to_sheet(data, batch_size=5):
    """Append job data to Google Sheet in batches."""
    if not data:
        return

    try:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            sheets_limiter.wait()
            sheet.append_rows(batch)
            print(f"Saved batch of {len(batch)} rows to sheet")
            time.sleep(2)  # Increased delay between batches
        
        print(f"Successfully saved all {len(data)} rows to sheet")
    except Exception as e:
        print(f"Error saving to sheet: {e}")
        raise

def search_twitter_jobs():
    """Search Twitter for tech job tweets and upload to Google Sheets."""
    job_data = []
    start_time = get_valid_start_time()
    
    print(f"Starting search from {start_time}")

    try:
        existing_urls = get_existing_urls()
        print(f"Found {len(existing_urls)} existing URLs in sheet")
    except Exception as e:
        print(f"Error fetching existing URLs: {e}")
        return

    for term in search_terms:
        print(f"\nSearching for term: {term}")
        try:
            # Use the wrapper function for Twitter API requests
            tweets = handle_twitter_request(
                client.search_recent_tweets,
                query=f"{term} -is:retweet",
                tweet_fields=['created_at', 'author_id', 'text'],
                user_fields=['username'],
                expansions=['author_id'],
                max_results=num_tweets,
                start_time=start_time
            )
            
            if not tweets.data:
                print(f"No tweets found for {term}")
                continue

            users = {user.id: user for user in tweets.includes['users']} if tweets.includes else {}
            
            for tweet in tweets.data:
                try:
                    author = users.get(tweet.author_id)
                    if not author:
                        continue

                    job_url = f"https://twitter.com/{author.username}/status/{tweet.id}"
                    
                    if job_url in existing_urls:
                        print(f"Skipping duplicate tweet: {job_url}")
                        continue

                    job_data.append([
                        author.username,
                        tweet.text,
                        job_url,
                        tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ])
                    print(f"Found new tweet: {job_url}")

                except Exception as e:
                    print(f"Error processing tweet: {e}")

            time.sleep(5)  # Increased delay between searches

        except Exception as e:
            print(f"Error searching term '{term}': {e}")
            time.sleep(15)  # Added delay after errors
            continue

    if job_data:
        try:
            save_to_sheet(job_data)
            notification_message = f"{len(job_data)} new tech jobs added to the Google Sheet."
            send_notifications(notification_message)
            print(notification_message)
        except Exception as e:
            print(f"Error saving data: {e}")
    else:
        print("No new jobs found.")

if __name__ == "__main__":
    try:
        search_twitter_jobs()
    except KeyboardInterrupt:
        print("\nScript terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")