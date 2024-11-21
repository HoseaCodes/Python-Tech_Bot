import time
import math
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries=5):
    """
    Decorator to add retry logic with exponential backoff to a function.
    
    Args:
        max_retries (int): Maximum number of retry attempts.
    """
    def decorator(func):
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
    return decorator
