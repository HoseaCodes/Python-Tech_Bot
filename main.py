import logging
import config
import time
import math
from TwitterClient import TwitterClient
from GoogleSheet import GoogleSheetsClient
from RateLimiter import RateLimiter
from Util import Util

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Retry decorator with exponential backoff
def retry_with_backoff(func, max_retries=5):
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                wait_time = math.pow(2, retries)
                logger.warning(f"Error in {func.__name__}: {e}. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                retries += 1
        raise Exception(f"Max retries reached for {func.__name__}.")
    return wrapper

# Main function
def main():
    twitter_client = TwitterClient(config)
    sheets_client = GoogleSheetsClient("service_account_credentials.json", "TechJobs")
    rate_limiter = RateLimiter(60)

    search_terms = ["#techjobs", "#breakintotech", "#BackendEngineer", "#startupjob", "#RemoteWork"]
    query = f"{search_terms[0]} lang:en -is:retweet"
    max_results = 10

    start_time = Util.get_start_time(days_ago=1)

    try:
        # Fetch tweets with retry
        tweets = fetch_tweets_with_retry(
            twitter_client=twitter_client,
            query=query,
            max_results=max_results,
            start_time=start_time
        )

        if not tweets or not tweets.data:
            logger.info("No tweets found.")
            return

        rows = [Util.map_tweet_to_row(tweet) for tweet in tweets.data if Util.map_tweet_to_row(tweet)]
        if rows:
            # Save rows to Google Sheets with retry
            save_rows_with_retry(sheets_client, rows, rate_limiter)
            logger.info(f"Successfully saved {len(rows)} rows to the Google Sheet.")
        else:
            logger.info("No valid rows to save.")
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)

# Fetch tweets with retry logic
@retry_with_backoff
def fetch_tweets_with_retry(twitter_client, query, max_results, start_time):
    return twitter_client.search_tweets(
        query=query,
        max_results=max_results,
        start_time=start_time,
        expansions="geo.place_id",
        place_fields="country_code",
        tweet_fields=["created_at", "text"]
    )

# Save rows to Google Sheets with retry logic
@retry_with_backoff
def save_rows_with_retry(sheets_client, rows, rate_limiter):
    sheets_client.save_rows(rows, rate_limiter)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    except Exception as e:
        logger.critical(f"Unexpected fatal error: {e}", exc_info=True)
