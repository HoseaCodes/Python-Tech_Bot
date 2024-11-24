import json
import time
import tweepy
import logging
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TwitterClient:
    def __init__(self, config):
        self.client = tweepy.Client(
            bearer_token=config.BEARER_TOKEN,
            consumer_key=config.CONSUMER_KEY,
            consumer_secret=config.CONSUMER_SECRET,
            access_token=config.ACCESS_KEY,
            access_token_secret=config.ACCESS_SECRET,
            wait_on_rate_limit=True
        )

    def search_tweets(self, query, max_results, start_time, place_fields=None, expansions=None, tweet_fields=None):
        try:
            return self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                start_time=start_time,
                expansions=expansions,
                place_fields=place_fields,
                tweet_fields=tweet_fields
            )
        except tweepy.TooManyRequests:
            logger.warning("Rate limit hit, sleeping for 15 minutes...")
            time.sleep(900)
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return None

