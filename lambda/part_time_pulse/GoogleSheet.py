import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    def __init__(self, creds_file, sheet_name):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def save_rows(self, rows, rate_limiter):
        try:
            rate_limiter.wait()
            self.sheet.append_rows(rows)
            logger.info(f"Successfully saved {len(rows)} rows to Google Sheets.")
        except Exception as e:
            logger.error(f"Error saving rows to Google Sheets: {e}")

