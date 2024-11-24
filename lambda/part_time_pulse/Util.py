
import json
import time
from datetime import datetime, timedelta, timezone
import logging
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Util:
    @staticmethod
    def get_start_time(days_ago=1):
        current_time = datetime.now(timezone.utc)
        start_time = current_time - timedelta(days=days_ago)
        return start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    @staticmethod
    def map_tweet_to_row(tweet):
        try:
            text = tweet.text
            hashtags = ", ".join([f"#{tag}" for tag in text.split() if tag.startswith("#")])
            links = ", ".join([word for word in text.split() if word.startswith("http")])
            title = text.split("\n")[0]
            date_pulled = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            return [title, "N/A", links, "N/A", date_pulled, "No", "No", hashtags]
        except Exception as e:
            raise ValueError(f"Error mapping tweet: {e}")