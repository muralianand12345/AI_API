from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from ..utils.error_handler import AIApiException
from ..utils.models import ChatMessage, ChatResponse
from ..utils.auth import get_current_user
from ..utils.database import DBUser
from ..utils.files_manager import pdf_manager
from config import Config

router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...), current_user: DBUser = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        file_path = await pdf_manager.save_pdf(file, current_user.username)
        chunks = pdf_manager.process_pdf(file_path, current_user.username)

        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "chunks_processed": len(chunks),
        }
    except Exception as e:
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
        relevant_docs = pdf_manager.search_documents(current_user.username, message.message)

        context = "\n\n".join(relevant_docs) if relevant_docs else ""

        if context:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", Config.Prompt.default),
                    ("system", f"Context from user documents:\n{context}"),
                    ("user", "{input}"),
                ]
            )
        else:
            prompt = ChatPromptTemplate.from_messages(
                [("system", Config.Prompt.default), ("user", "{input}")]
            )

        chain = prompt | Config.Model.llm
        ai_response = chain.invoke({"input": message.message})
        response_content = (
            ai_response.content if hasattr(ai_response, "content") else str(ai_response)
        )

        return ChatResponse(
            username=current_user.username,
            message=message.message,
            response=response_content,
        )
    except Exception as e:
        raise AIApiException(detail="Error occurred while chatting with AI, try again.", error=str(e))