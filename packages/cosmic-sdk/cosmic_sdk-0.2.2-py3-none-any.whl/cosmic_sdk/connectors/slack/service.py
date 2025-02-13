from .client import SlackClient
class SlackService:
    def __init__(self, credentials: dict):
        self.client = SlackClient(credentials)

    def get_channel_history(self, channel: str, limit: int = 100, oldest: str = None, latest: str = None, inclusive: bool = True):
        return self.client.get_channel_history(channel, limit, oldest, latest, inclusive)
    
    def send_message(self, channel: str, message: str):
        return self.client.send_message(channel, message)
    




    
