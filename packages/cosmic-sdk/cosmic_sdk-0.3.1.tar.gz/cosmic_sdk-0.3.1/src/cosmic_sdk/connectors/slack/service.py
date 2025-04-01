import logging
#from cosmic_sdk.connectors.posthog.models import Group, User, Event
import requests
import sys
import os
#from .models import SlackCredentials, SlackMessage, SlackHistoryRequest, SlackMessageResponse, SlackHistoryResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Ref: https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/
logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self, credentials: dict):
        try:
            self.client = WebClient(token=credentials['slack_bot_token'])
            self.channel_id = ''
        except Exception as e:
            raise ValueError(f"Failed to initialize Slack client: {str(e)}")
        

    def set_channel_id(self, channel_id: str):
        self.channel_id = channel_id

    def get_channel_id(self):
        return self.channel_id


    def get_token(self):
        return self.client.token
    
    
    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(
                channel=message.channel_id, 
                text=message.text
            )
            return response
        except SlackApiError as e:
            raise ValueError(f"Failed to send message: {str(e)}")
        
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
        


    
