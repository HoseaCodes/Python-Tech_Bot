import time
from datetime import datetime, timedelta
import config
import requests
import logging
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail, SendSmtpEmailTo, TransactionalSMSApi

import http.client as http_client

http_client.HTTPConnection.debuglevel = 1  # Enable HTTP debug output
logging.getLogger("urllib3").setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Brevo:
    def __init__(self):
        # Brevo (Sendinblue) setup
        self.BREVO_API_KEY = config.BREVO_API_KEY
        self.BREVO_SMS_SENDER = config.BREVO_SMS_SENDER
        self.BREVO_SMS_RECIPIENT = config.BREVO_SMS_RECIPIENT
        self.SENDER_EMAIL = config.EMAIL_ADDRESS
        self.RECIPIENT_EMAIL = config.RECIPIENT_EMAIL
        
        # Configure API client
        self.configuration = Configuration()
        self.configuration.api_key['api-key'] = self.BREVO_API_KEY
        
    def send_email(self, subject, body):
        """Send email using Brevo's API."""
        try:
            api_client = ApiClient(self.configuration)
            api_instance = TransactionalEmailsApi(api_client)
            
            to = [SendSmtpEmailTo(email=self.RECIPIENT_EMAIL)]
            send_email = SendSmtpEmail(
                sender={"email": self.SENDER_EMAIL},
                to=to,
                subject=subject,
                html_content=body
            )
            
            api_response = api_instance.send_transac_email(send_email)
            logger.info(f"Email sent successfully! Message ID: {api_response.message_id}")
        
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")

    def send_sms(self, message):
        """Send SMS using Brevo's API (sib_api_v3_sdk)."""
        try:
            api_client = ApiClient(self.configuration)
            sms_api_instance = TransactionalSMSApi(api_client)

            send_sms = {
                'sender': self.BREVO_SMS_SENDER,
                'recipient': self.BREVO_SMS_RECIPIENT,
                'content': message,
            }

            api_response = sms_api_instance.send_transac_sms(send_sms)
            logger.info(f"SMS sent successfully! Message ID: {api_response.message_id}")

        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")