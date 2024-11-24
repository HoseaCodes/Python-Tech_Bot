Here's the updated README with all the requested links added:

---

# Tech Job Scraper Bot

A Python-based bot that fetches tech job tweets, saves them to Google Sheets, and sends email/SMS notifications about updates. Built with Twitter API, Google Sheets API, and Brevo (Sendinblue).

---

## Features

- **Fetch tweets**: Searches Twitter for job-related hashtags and terms.
- **Save to Google Sheets**: Stores job details in a structured Google Sheet.
- **Email and SMS notifications**: Sends updates and alerts using Brevo.

---

## Configuration

The project requires a `config.py` file to store your API keys and credentials. Below is the structure of the `config.py` file:

```python
# Twitter setup
CONSUMER_KEY = ''  # API Key
CONSUMER_SECRET = ''  # API Secret
ACCESS_KEY = ''  # API Token
ACCESS_SECRET = ''  # API Token Secret
BEARER_TOKEN = ''  # Bearer Token

# Email setup
SMTP_SERVER = ''  # SMTP server address (e.g., smtp.gmail.com)
SMTP_PORT = 587  # SMTP server port (typically 587 for TLS)
EMAIL_ADDRESS = ''  # Your email address
EMAIL_PASSWORD = ''  # Your email password or app-specific password
RECIPIENT_EMAIL = ''  # Recipient's email address for notifications

# Brevo (Sendinblue) setup
BREVO_API_KEY = ''  # Brevo (Sendinblue) API Key
BREVO_SMS_SENDER = ''  # Brevo-approved sender name/ID for SMS
BREVO_SMS_RECIPIENT = ''  # Phone number of SMS recipient

# Brevo API configuration
BREVO_API_URL = 'https://api.brevo.com/v3/'  # Brevo API base URL
BREVO_SMS_TYPE = 'transactional'  # Type of SMS (e.g., transactional or promotional)
```

---

## Requirements

- Python 3.8 or higher
- Twitter Developer Account for API access
- Google Sheets API credentials
- Brevo (Sendinblue) account for email/SMS notifications

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HoseaCodes/Python-Tech_Bot
   cd Python-Tech_Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the `config.py` file**:
   Create a `config.py` file in the project root directory with the structure mentioned above.

4. **Google Sheets Setup**:
   - Create a Google Cloud project and enable the [Google Sheets API](https://console.cloud.google.com/apis/api/sheets.googleapis.com/metrics?authuser=1&project=coldemail-433504).
   - Download the `service_account_credentials.json` file and place it in the project root.

---

## Usage

1. **Run locally**:
   ```bash
   python main.py
   ```

2. **Deploy on AWS Lambda**:
   - Package the code using the provided build script.
   - Upload the `function.zip` to your [Lambda function](https://us-east-2.console.aws.amazon.com/lambda/home?region=us-east-2#/functions/PartTimePulse?tab=code).
   - Set up environment variables to match the keys in `config.py`.

---

## Links

- **Twitter API Documentation**:
  - [Twitter Place Object Model](https://developer.x.com/en/docs/x-api/data-dictionary/object-model/place)
  - [Build a Twitter Query](https://developer.x.com/en/docs/x-api/tweets/search/integrate/build-a-query)
- **GitHub Repository**: [Tech Job Scraper Bot](https://github.com/HoseaCodes/Python-Tech_Bot)
- **Google Cloud Console**: [Google Sheets API Metrics](https://console.cloud.google.com/apis/api/sheets.googleapis.com/metrics?authuser=1&project=coldemail-433504) *(Must Request Access)*
- **Google Sheet**: [Job Listings Sheet](https://docs.google.com/spreadsheets/d/1aGaGfPucJ-hmmnDHWZs2YQ2sF2IhE3H6PPw-_OiC38Y) *(Must Request Access)*
- **Brevo (Sendinblue)**: [Real-Time API](https://app-smtp.brevo.com/real-time) *(Must Request Access)*
- **AWS Lambda Console**: [PartTimePulse Lambda Function](https://us-east-2.console.aws.amazon.com/lambda/home?region=us-east-2#/functions/PartTimePulse?tab=code) *(Must Request Access)*

---

## Fetch Tweets

The project uses the `search_recent_tweets` method from Tweepy to fetch tweets based on specified hashtags and terms. For more details, refer to the [Tweepy `search_recent_tweets` documentation](https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets).

---

## Functionality Overview

- **Fetch tweets**: Uses the Twitter API to retrieve recent tweets containing specified hashtags and job-related terms.
- **Retry logic**: Implements exponential backoff for resilient API requests.
- **Save to Google Sheets**: Maps tweet data to a row format and appends it to a Google Sheet.
- **Notification system**: Alerts users via email and SMS when new job listings are saved or when an error occurs.

---

## Contact

For questions or contributions, contact **HoseaCodes** at [info@ambitiousconcept.com](mailto:info@ambitiousconcept.com).

--- 