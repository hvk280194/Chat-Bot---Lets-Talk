from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Conversation session id")
    message: str

class ChatResponse(BaseModel):
    session_id: str
    output: str
    meta: Optional[Dict[str, Any]] = None
