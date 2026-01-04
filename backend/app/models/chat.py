from pydantic import BaseModel
from typing import Optional, List

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    message_id: Optional[str] = None
