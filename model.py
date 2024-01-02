from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    session_id: int
    message: str
    bot_reply: str

class SessionID(BaseModel):
    session_id: int

class messageChatbot(BaseModel):
    session_id: int
    message: str
