from pydantic import BaseModel
from typing import List, Optional

class VisualStat(BaseModel):
    category: str
    count: int
    avg_views: float

class ChannelStat(BaseModel):
    channel: str
    posts: int
    avg_views: float

class MessageSearch(BaseModel):
    channel_name: str
    message_text: str
    view_count: int