# posthog/client.py
# Purpose: Interacts with the Slack API and fetch or manipulate data.
import logging
from typing import List, Dict, Any
#from cosmic_sdk.connectors.posthog.models import Group, User, Event
import requests
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Ref: https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/

class SlackClient:
    def __init__(self, credentials: dict):
        try:
            slack_token = credentials.get('slackToken') or credentials.get('slack_token')
            self.client = WebClient(token=slack_token)
            self.channel_id = ''
            
            if not slack_token:
                raise ValueError("Missing required credential: 'slackToken' or 'slack_token'")
        except Exception as e:
            raise ValueError(f"Failed to initialize Slack client: {str(e)}")
        

    def set_channel_id(self, channel_id: str):
        self.channel_id = channel_id

    def get_channel_id(self):
        return self.channel_id


    def get_token(self):
        return self.client.token
    
    
    def send_message(self, message: str):
        try:
            response = self.client.chat_postMessage(channel=self.channel_id, text=message)
            return response['message']['ts']
        except SlackApiError as e:
            raise ValueError(f"Failed to send message: {str(e)}")
        
    def get_channel_history(
            self, 
            channel: str, # channel id
            limit: int = 100,  # optional - number of messages to return
            oldest: str = None,  # optional - oldest message timestamp to include
            latest: str = None,  # optional - newest message timestamp to include
            inclusive: bool = True  # optional - include messages with the oldest or newest timestamp
        ):
        try:
            response = self.client.conversations_history(
                channel=channel,
                limit=limit,
                oldest=oldest,
                latest=latest,
                inclusive=inclusive
            )
            return response['messages']
        except SlackApiError as e:
            raise ValueError(f"Failed to get channel history: {str(e)}")
        
        
    
    
    
