import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration for the Q&A System."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # File Paths
    DATA_DIR = os.getenv("DATA_DIR", "data")
    
    # Model Configurations
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Access Control Mapping (Dummy Users)
    USERS = {
        "alice@email.com": ["Company_A"],
        "bob@email.com": ["Company_B", "Company_C"],
        "charlie@email.com": ["Company_D", "Company_E"]
    }
