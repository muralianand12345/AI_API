from pydantic import BaseModel
from typing import List

class UserLogin(BaseModel):
    username: str
    password: str

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    username: str
    message: str
    response: str
    
    class Config:
        from_attributes = True

class DocumentStats(BaseModel):
    total_documents: int
    has_embeddings: bool

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_processed: int