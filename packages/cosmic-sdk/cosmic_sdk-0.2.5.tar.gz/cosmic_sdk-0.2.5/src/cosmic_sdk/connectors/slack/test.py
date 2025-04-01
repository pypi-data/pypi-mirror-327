from cosmic_sdk.connectors import SlackService

if __name__ == "__main__":
    # Create credentials dictionary with your Slack bot token
    credentials = {
        "slack_bot_token": "xo-xo"  # Replace with your actual token
    }
    
    # Initialize the service
    slack_service = SlackService(credentials)
    
    # Test our slack service
    channel_id = "xoxoxo"  # Replace with actual channel ID
    slack_service.set_channel_id(channel_id)
    slack_service.send_message("Hello from cosmic_sdk!")
    slack_service.get_channel_history(channel_id)