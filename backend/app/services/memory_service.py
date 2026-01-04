from typing import List, Dict
from datetime import datetime, timedelta
import json

class MemoryService:
    """
    Manages conversation history.
    
    Options:
    - In-memory storage (development)
    - Redis (production - recommended)
    - Database (PostgreSQL/MongoDB)
    """
    
    def __init__(self):
        # Simple in-memory store (use Redis in production)
        self.conversations: Dict[str, List[Dict]] = {}
        self.ttl = timedelta(hours=24)  # Auto-expire after 24h
    
    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """
        Retrieve conversation history in Gemini format.
        
        Returns:
            [
                {"role": "user", "parts": ["Hello"]},
                {"role": "model", "parts": ["Hi! How can I help?"]},
                ...
            ]
        """
        return self.conversations.get(conversation_id, [])
    
    def add_exchange(
        self,
        conversation_id: str,
        user_message: str,
        ai_response: str
    ):
        """Add new message exchange to memory."""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].extend([
            {
                "role": "user",
                "parts": [user_message],
                # "timestamp": datetime.utcnow().isoformat() # Gemini API might strictly validate roles/parts, better to keep metadata separate or ensuring it doesn't break API call if passed directly.
                # Keeping it simple for Gemini compatibility
            },
            {
                "role": "model",
                "parts": [ai_response],
                # "timestamp": datetime.utcnow().isoformat()
            }
        ])
    
    def clear_conversation(self, conversation_id: str):
        """Delete conversation history."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
