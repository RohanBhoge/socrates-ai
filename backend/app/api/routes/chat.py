from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import uuid
from app.services.gemini_service import GeminiService
from app.services.file_processor import FileProcessor
from app.models.chat import ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])
gemini_service = GeminiService()

@router.post("", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    files: List[UploadFile] = File(None)
):
    """
    Main chat endpoint.
    """
    try:
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Process files
        processed_files = []
        if files:
            for file in files:
                processed_file = await FileProcessor.process_upload(file)
                processed_files.append(processed_file)
        
        # Get response from Gemini
        reply = await gemini_service.generate_response(
            user_message=message,
            conversation_id=conversation_id,
            files=processed_files
        )
        
        return ChatResponse(
            reply=reply,
            conversation_id=conversation_id,
            message_id=str(uuid.uuid4())
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    """
    Retrieve full conversation history.
    """
    history = gemini_service.memory.get_conversation(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": history
    }

@router.post("/clear/{conversation_id}")
async def clear_memory(conversation_id: str):
    """Clear conversation memory for a session."""
    gemini_service.memory.clear_conversation(conversation_id)
    return {"status": "success", "message": "Memory cleared"}
