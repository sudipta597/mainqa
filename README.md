# Multi-User Document Search and Conversational Q&A System

This project is a multi-user document search system that allows users to query a collection of text documents and retrieve relevant excerpts based on their queries. 
The system ensures that each user has restricted access to specific documents, retrieving answers only from authorized files. It features a conversational Q&A experience maintaining context from previous interactions.

## Architecture & Code Structure
The system has been refactored into a scalable Object-Oriented architecture with clear separation of concerns.

```text
multi_user_qa_system/
├── app.py                     # Main Streamlit application UI
├── data/                      # Generated PDF documents (auto-generated)
├── .env                       # Environment variables (Create this from .env.example)
├── .env.example               # Template for environment variables
├── requirements.txt           # Python dependencies
├── run.bat                    # Windows execution script
├── run.sh                     # Linux/Mac execution script
├── test_system.py             # CLI test script for validation
└── utils/                     # Core logic modules
    ├── __init__.py
    ├── auth.py                # User authentication and access control mapping
    ├── config.py              # Configuration and environment variable management
    ├── document_manager.py    # PDF loading, splitting, vector store (FAISS), and embeddings
    └── chat_engine.py         # Conversational retrieval chain and memory management
```

## Features
- **Multi-User Login:** Simulate login with mock emails.
- **Document Access Control:** 
  - `alice@email.com` -> Company A
  - `bob@email.com` -> Company B, Company C
  - `charlie@email.com` -> Company D, Company E
- **Conversational Experience:** Remembers past queries for context-aware Q&A.
- **Data Privacy:** Guaranteed isolation of queries and documents per user using scoped Vector Stores.
- **Google GenAI Integration:** Uses Gemini models for both responses (Gemini 1.5 Flash) and high-quality embeddings (`models/embedding-001`).

## Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed.

### 2. API Key Configuration
Create a `.env` file in the root of the project by copying `.env.example`, and add your Google API key:
```bash
cp .env.example .env
```
Update the `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
```
*Note: Both text generation and text embeddings require a valid Google API key.*

### 3. Run the Application Easy Way (Automated Scripts)
You can easily setup the virtual environment, install dependencies, generate dummy PDFs, and launch the app using the provided scripts.

**For Windows:**
Double click on `run.bat` or execute in terminal:
```cmd
.\run.bat
```

**For Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

### 4. Run the Application Manual Way
If you prefer to set it up manually:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 5. Testing the Solution via UI
1. The app will open in your browser (usually `http://localhost:8501`).
2. In the sidebar, log in as `alice@email.com`.
3. Ask a question like "What is the revenue for Company A?".
4. Try to ask "What is the revenue for Company B?". (It should not have access).
5. Follow up with "Who is the CEO?". It will use conversational context to know you are talking about Company A.
6. Logout and login as `bob@email.com` to test multi-company access (Company B & C).

### 6. Testing via CLI (Headless)
You can also verify the access control and conversational logic by running the automated CLI test script:
```bash
python test_system.py
```

## Technical Stack
- **Frontend:** Streamlit
- **Document Processing:** LangChain (`PyPDFLoader`, `RecursiveCharacterTextSplitter`)
- **Embeddings:** Google Generative AI Embeddings (`models/embedding-001`)
- **Vector Database:** FAISS (In-memory, CPU friendly)
- **LLM:** Google Generative AI (`gemini-2.5-flash`) via LangChain's `ConversationalRetrievalChain`
