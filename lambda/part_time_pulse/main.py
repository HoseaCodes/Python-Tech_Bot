import logging
import config
from TwitterClient import TwitterClient
from GoogleSheet import GoogleSheetsClient
from RateLimiter import RateLimiter
from Util import Util
from Brevo import Brevo
from datetime import datetime, timedelta
from RetryUtil import retry_with_backoff 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Main function
def main():
    twitter_client = TwitterClient(config)
    sheets_client = GoogleSheetsClient("service_account_credentials.json", "TechJobs")
    rate_limiter = RateLimiter(60)
    email_client = Brevo()

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
            email_body = f"""
            Hello,

            We have successfully updated the Google Sheet with new tech job listings. 

            Details:
            - Number of new job listings: {len(rows)}
            - Search terms used: {', '.join(search_terms)}
            - Time of update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            The new job listings have been mapped from recent tweets and saved to the sheet.

            Thank you for using our service!

            Best regards,
            Your Tech Job Bot
            """
            email_client.send_email("Google Sheet Updated", email_body)
            email_client.send_sms(f"{len(rows)} new tech jobs added to the Google Sheet.")
        else:
            logger.info("No valid rows to save.")
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        error_body = f"""
        Hello,

        An error occurred during the execution of fetching Twitter data for tech jobs. 

        Error Details:
        - Error message: {str(e)}
        - Time of error: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Please review the logs for further troubleshooting.

        Best regards,
        Your Tech Job Bot
        """
        email_client.send_email("Error during execution of fetching twitter info", error_body)
        email_client.send_sms("Error during execution of fetching Twitter data for tech jobs. Please review the logs for further troubleshooting.")

# Fetch tweets with retry logic
@retry_with_backoff(max_retries=5)
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
@retry_with_backoff(max_retries=5)
def save_rows_with_retry(sheets_client, rows, rate_limiter):
    sheets_client.save_rows(rows, rate_limiter)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    except Exception as e:
        logger.critical(f"Unexpected fatal error: {e}", exc_info=True)

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    main()
    return {
        "statusCode": 200,
        "body": "Job scraping completed successfully!"
    }