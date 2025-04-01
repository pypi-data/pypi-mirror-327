import logging
#from cosmic_sdk.connectors.posthog.models import Group, User, Event
import requests
import sys
import os
#from .models import SlackCredentials, SlackMessage, SlackHistoryRequest, SlackMessageResponse, SlackHistoryResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Ref: https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/
# Configure logging at the top of the file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self, credentials: dict):
        try:
            logger.info("Initializing SlackService...")
            logger.info(f"Received credentials type: {type(credentials)}")
            logger.info(f"Received credentials: {credentials}")
            
            self.credentials = credentials
            token = self.credentials.get('slack_bot_token')
            logger.info(f"Retrieved token: {token}")
            
            self.client = WebClient(token=token)
            self.channel_id = ''

            logger.info("Initialization complete")
            logger.info(f"Final credentials: {self.credentials}")
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            raise ValueError(f"Failed to initialize Slack client: {str(e)}")

    def set_channel_id(self, channel_id: str):
        self.channel_id = channel_id

    def get_channel_id(self):
        return self.channel_id

    def get_token(self):
        return self.client.token
    
    def send_message(self, message: str):
        logger.info(f"Self type: {type(self)}")  # Debug print
        logger.info(f"Self dict: {self.__dict__}")  # Debug print

        if self.channel_id is None:
            raise ValueError("Channel ID is not set. Please call set_channel_id first.")
            
        if self.client is None:
            raise ValueError("Slack client is not initialized. Please call initialize_client first.")
        
        response = self.client.chat_postMessage(
            channel=self.channel_id,
            text=message
        )
        return response
        
    def get_channel_history(self, request):
        try:
            response = self.client.conversations_history(
                channel=request.channel,
                limit=request.limit,
                oldest=request.oldest,
                latest=request.latest,
                inclusive=request.inclusive
            )
            return response
        except SlackApiError as e:
            raise ValueError(f"Failed to get channel history: {str(e)}")
        

    

