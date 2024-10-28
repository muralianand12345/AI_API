from typing import Dict
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from ..utils.error_handler import AIApiException
from ..utils.models import ChatMessage, ChatResponse
from ..utils.auth import get_current_user
from ..utils.database import DBUser
from ..utils.files_manager import pdf_manager
from ..utils.logger import logger
from config import Config

router = APIRouter()

user_memories: Dict[str, ConversationBufferMemory] = {}

def get_or_create_memory(username: str) -> ConversationBufferMemory:
    """Get or create a memory instance for a user."""
    if username not in user_memories:
        user_memories[username] = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            input_key="input",
            output_key="output"
        )
    return user_memories[username]

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...), current_user: DBUser = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        if logger:
            logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        if logger:
            logger.info(f"Processing PDF: {file.filename}")
        file_path = await pdf_manager.save_pdf(file, current_user.username)
        chunks = pdf_manager.process_pdf(file_path, current_user.username)

        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "chunks_processed": len(chunks),
        }
    except Exception as e:
        if logger:
            logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/documents/stats")
async def get_document_stats(current_user: DBUser = Depends(get_current_user)):
    return pdf_manager.get_user_stats(current_user.username)


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI using RAG",
    description="Send a message to the AI and get a response with context from your documents",
)
async def chat(message: ChatMessage, current_user: DBUser = Depends(get_current_user)):
    try:
        if logger:
            logger.info(f"Chatting with AI: {message.message}")
            
        memory = get_or_create_memory(current_user.username)
        
        relevant_docs = pdf_manager.search_documents(
            current_user.username, message.message
        )

        context = "\n\n".join(relevant_docs) if relevant_docs else ""
        
        messages = [("system", Config.Prompt.default)]
        if context:
            messages.append(("system", f"Context from user documents:\n{context}"))

        chat_history = memory.load_memory_variables({}).get("chat_history", [])
        if chat_history:
            messages.extend([
                ("human" if isinstance(msg, HumanMessage) else "assistant", msg.content)
                for msg in chat_history[-Config.Memory.buffer_size:]
            ])
            
        messages.append(("user", "{input}"))
        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | Config.Model.llm | StrOutputParser()
        ai_response = chain.invoke({"input": message.message})
        response_content = (
            ai_response.content if hasattr(ai_response, "content") else str(ai_response)
        )
        
        memory.save_context(
            {"input": message.message},
            {"output": response_content}
        )

        if logger:
            logger.info(f"AI response: {response_content}")

        return ChatResponse(
            username=current_user.username,
            message=message.message,
            response=response_content,
        )
    except Exception as e:
        if logger:
            logger.error(f"Error chatting with AI: {str(e)}")
        raise AIApiException(
            detail="Error occurred while chatting with AI, try again.", error=str(e)
        )

@router.delete("/chat/history")
async def clear_chat_history(current_user: DBUser = Depends(get_current_user)):
    """Clear the chat history for a user."""
    try:
        if current_user.username in user_memories:
            del user_memories[current_user.username]
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        if logger:
            logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error clearing chat history")