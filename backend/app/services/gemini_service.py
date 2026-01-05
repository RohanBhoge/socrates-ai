import google.generativeai as genai
from typing import List, Optional
from app.core.system_prompt import SOCRATES_SYSTEM_PROMPT
from app.services.memory_service import MemoryService
from app.config import settings

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            print("GEMINI_API_KEY: ", settings.GEMINI_API_KEY)  
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                system_instruction=SOCRATES_SYSTEM_PROMPT
            )
        else:
            print("Warning: GEMINI_API_KEY not found in settings.")
            self.model = None

        self.memory = MemoryService()
    
    async def generate_response(
        self,
        user_message: str,
        conversation_id: str,
        files: Optional[List[dict]] = None
    ) -> str:
        """
        Generate Socratic response using Gemini.
        
        Process:
        1. Retrieve conversation history from memory
        2. Build prompt with context
        3. Include uploaded files (if any)
        4. Call Gemini API
        5. Store new exchange in memory
        6. Return response
        """
        if not self.model:
            return "Error: Gemini API key not configured."

        # 1. Get conversation history
        history = self.memory.get_conversation(conversation_id)
        
        # 2. Build message content
        message_parts = [user_message]
        
        # 3. Add file data if present
        # files expected to be a list of dictionaries with 'mime_type' and 'data' (bytes) 
        # OR just bytes if we handle it that way. The spec said "files: List[bytes]".
        # However, genai usually expects parts.
        # Let's assume files is list of processed objects compatible with Gemini or we convert them here.
        if files:
            for file_data in files:
                # Assuming file_data is compatible object or bytes
                message_parts.append(file_data)
        
        # 4. Create chat session with history
        # Note: history must be cleanly formatted for Gemini
        chat = self.model.start_chat(history=history)
        
        # 5. Generate response
        try:
             response = await chat.send_message_async(message_parts)
             response_text = response.text
        except Exception as e:
             return f"Error generating response: {str(e)}"
        
        # 6. Store in memory
        self.memory.add_exchange(
            conversation_id,
            user_message=user_message,
            ai_response=response_text
        )
        
        return response_text
