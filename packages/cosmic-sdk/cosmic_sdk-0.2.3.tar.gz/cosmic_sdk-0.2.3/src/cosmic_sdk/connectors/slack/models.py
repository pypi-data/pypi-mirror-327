from pydantic import BaseModel, Field
from typing import Optional, List

class SlackCredentials(BaseModel):
    slack_bot_token: str = Field(..., description="Slack Bot User OAuth Token")

class SlackMessage(BaseModel):
    channel_id: str = Field(..., description="Slack channel ID")
    text: str = Field(..., description="Message text to send")

class SlackHistoryRequest(BaseModel):
    channel: str = Field(..., description="Channel ID to fetch history from")
    limit: Optional[int] = Field(100, description="Number of messages to return", ge=1, le=1000)
    oldest: Optional[str] = Field(None, description="Start of time range (timestamp)")
    latest: Optional[str] = Field(None, description="End of time range (timestamp)")
    inclusive: Optional[bool] = Field(True, description="Include messages with oldest/latest timestamps")

class SlackMessageResponse(BaseModel):
    ok: bool
    ts: str = Field(..., description="Timestamp of the message")
    message: dict = Field(..., description="Message details")
    channel: str = Field(..., description="Channel ID where message was sent")

class SlackHistoryResponse(BaseModel):
    ok: bool
    messages: List[dict] = Field(..., description="List of messages in the channel")
    has_more: bool = Field(..., description="Whether there are more messages to fetch")
