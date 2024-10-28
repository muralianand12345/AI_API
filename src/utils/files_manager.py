import os
from typing import List, Dict
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from fastapi import UploadFile
from .database import DBUser
from config import Config
from .logger import logger

class PDFManager:
    def __init__(self):
        self.user_embeddings: Dict[str, FAISS] = {}
        self.base_path = os.path.join(Config.Data.folder, "pdfs")
        os.makedirs(self.base_path, exist_ok=True)
    
    def get_user_folder(self, username: str) -> str:
        user_folder = os.path.join(self.base_path, username)
        os.makedirs(user_folder, exist_ok=True)
        if logger:
            logger.info(f"User folder created: {user_folder}")
        return user_folder
    
    async def save_pdf(self, file: UploadFile, username: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(self.get_user_folder(username), filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        if logger:
            logger.info(f"PDF saved: {file_path}")
        
        return file_path
    
    def process_pdf(self, file_path: str, username: str) -> List[str]:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        if username not in self.user_embeddings:
            self.user_embeddings[username] = FAISS.from_documents(
                splits, 
                Config.Model.embedding
            )
        else:
            self.user_embeddings[username].add_documents(splits)
            
        if logger:
            logger.info(f"PDF processed: {file_path}")
        
        return [doc.page_content for doc in splits]
    
    def search_documents(self, username: str, query: str, k: int = 3) -> List[str]:
        if username not in self.user_embeddings:
            if logger:
                logger.warning(f"No embeddings found for user: {username}")
            return []
            
        docs = self.user_embeddings[username].similarity_search(query, k=k)
        
        if logger:
            logger.info(f"Search results for {username}: {docs}")
        
        return [doc.page_content for doc in docs]
    
    def get_user_stats(self, username: str) -> Dict:
        if username not in self.user_embeddings:
            if logger:
                logger.info(f"No embeddings found for user: {username}")
            return {"total_documents": 0, "has_embeddings": False}
        
        if logger:
            logger.info(f"User stats for {username}: {len(self.user_embeddings[username].docstore._dict)}")
            
        return {
            "total_documents": len(self.user_embeddings[username].docstore._dict),
            "has_embeddings": True
        }

pdf_manager = PDFManager()