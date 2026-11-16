# Multi-User Document Search and Conversational Q&A System

This project is a multi-user document search system that allows users to query a collection of text documents and retrieve relevant excerpts based on their queries. 
The system ensures that each user has restricted access to specific documents, retrieving answers only from authorized files. It features a conversational Q&A experience maintaining context from previous interactions.

## Features
- **Multi-User Login:** Simulate login with dummy emails.
- **Document Access Control:** 
  - `alice@email.com` -> Company A
  - `bob@email.com` -> Company B, Company C
  - `charlie@email.com` -> Company D, Company E
- **Conversational Experience:** Remembers past queries for context-aware Q&A.
- **Data Privacy:** Guaranteed isolation of queries and documents per user using scoped Vector Stores.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed.
- Ensure the required libraries are installed.

### 2. Install Dependencies
Run the following command to install the required packages:
```bash
pip install streamlit langchain langchain-community langchain-huggingface langchain-text-splitters faiss-cpu pypdf python-dotenv langchain-google-genai fpdf
```

### 3. Generate Sample Documents
First, generate the sample Earnings Call PDFs for Company A through E.
```bash
python generate_pdfs.py
```
This will create a `data/` directory with 5 PDF files.

### 4. API Key Configuration
To enable the full generative AI Conversational Q&A (using Google's Gemini), create a `.env` file in the same directory as `app.py` and add your Google API key:
```env
GOOGLE_API_KEY=your_google_api_key_here
```
*(If no API key is provided, the application will run in a graceful **MOCK MODE**, retrieving exact text chunks from the vector store instead of synthesizing generative responses, enabling you to test access controls and document retrieval.)*

### 5. Run the Application
Start the Streamlit UI server:
```bash
streamlit run app.py
```

### 6. Testing the Solution
1. Open the provided localhost URL in your browser.
2. In the sidebar, log in as `alice@email.com`.
3. Ask a question like "What is the revenue for Company A?".
4. Try to ask "What is the revenue for Company B?". (It should not have access).
5. Follow up with "Who is the CEO?". It will use conversational context to know you are talking about Company A.
6. Logout and login as `bob@email.com` to test multi-company access (Company B & C).

## Technical Architecture
- **Frontend:** Streamlit
- **Document Processing:** LangChain (`PyPDFLoader`, `RecursiveCharacterTextSplitter`)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Local, fast, free)
- **Vector Database:** FAISS (In-memory, CPU friendly)
- **LLM:** Google Generative AI (Gemini 1.5 Flash) via LangChain's `ConversationalRetrievalChain`
