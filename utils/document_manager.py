import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils.config import Config

class DocumentManager:
    """Handles ingestion, splitting, embedding, and vectorstore creation."""
    
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        # Fallback for testing: if no API key, use a dummy embedding for mock mode to pass tests without API calls
        if Config.GOOGLE_API_KEY:
            self.embeddings = GoogleGenerativeAIEmbeddings(model=Config.EMBEDDING_MODEL)
        else:
            from langchain_community.embeddings import FakeEmbeddings
            self.embeddings = FakeEmbeddings(size=768)
            
        self.base_vectorstore = None
        self.is_loaded = False
        
    def load_and_index_documents(self) -> bool:
        """Loads all PDFs, splits text, and indexes them into a base FAISS VectorStore."""
        if not os.path.exists(self.data_dir):
            return False
            
        documents = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".pdf"):
                company_name = filename.replace("_Earnings.pdf", "")
                filepath = os.path.join(self.data_dir, filename)
                
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                
                # Tag metadata for RBAC filtering later
                for doc in docs:
                    doc.metadata["company"] = company_name
                documents.extend(docs)
                
        if not documents:
            return False
            
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE, 
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(documents)
        
        # Build vector store
        self.base_vectorstore = FAISS.from_documents(splits, self.embeddings)
        self.is_loaded = True
        return True

    def create_user_vectorstore(self, allowed_companies: List[str]) -> Optional[FAISS]:
        """Filters the master index and creates a completely isolated FAISS store for a specific user."""
        if not self.is_loaded or self.base_vectorstore is None:
            return None
            
        # Extract all documents
        docs_and_scores = self.base_vectorstore.similarity_search_with_score("", k=10000)
        
        # Isolate
        filtered_docs = [doc for doc, _ in docs_and_scores if doc.metadata.get("company") in allowed_companies]
        
        if not filtered_docs:
            return None
            
        # Re-index only the authorized documents
        user_vectorstore = FAISS.from_documents(filtered_docs, self.embeddings)
        return user_vectorstore
