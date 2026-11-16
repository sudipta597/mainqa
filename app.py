import streamlit as st
from langchain_classic.memory import ConversationBufferMemory

from utils.auth import AuthManager
from utils.document_manager import DocumentManager
from utils.chat_engine import ChatEngine
from utils.config import Config

st.set_page_config(page_title="Multi-User Q&A System", page_icon="📄")

# 1. Initialize core managers (Cached heavily for performance)
@st.cache_resource
def load_global_documents():
    dm = DocumentManager()
    success = dm.load_and_index_documents()
    if not success:
        st.error(f"Failed to load documents from `{Config.DATA_DIR}`. Did you run `generate_pdfs.py`?")
        return None
    return dm

doc_manager = load_global_documents()
auth_manager = AuthManager()

# 2. Session State Initialization
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 3. Sidebar UI - Authentication
with st.sidebar:
    st.header("Login")
    st.write("Simulate login using dummy emails:")
    for email, companies in auth_manager.get_all_mock_users().items():
        st.write(f"- `{email}` (Access: {', '.join(companies).replace('_', ' ')})")
    
    email_input = st.text_input("Email Address")
    
    if st.button("Login"):
        if auth_manager.authenticate(email_input):
            st.session_state.logged_in_user = email_input
            st.session_state.chat_history = [] # Reset history on login
            st.session_state.memory.clear()
            st.success(f"Logged in as {email_input}")
            st.rerun()
        else:
            st.error("Invalid email address. Access denied.")
            
    if st.session_state.logged_in_user:
        current_user = st.session_state.logged_in_user
        allowed_companies = auth_manager.get_allowed_companies(current_user)
        st.write(f"**Current User:** {current_user}")
        st.write(f"**Access:** {', '.join(allowed_companies).replace('_', ' ')}")
        
        if st.button("Logout"):
            st.session_state.logged_in_user = None
            st.session_state.chat_history = []
            st.session_state.memory.clear()
            st.rerun()

# 4. Main Application Interface
st.title("Multi-User Document Q&A System")

if st.session_state.logged_in_user and doc_manager:
    user = st.session_state.logged_in_user
    allowed_companies = auth_manager.get_allowed_companies(user)
    
    st.write(f"Welcome, **{user}**. You can query documents from: {', '.join(allowed_companies).replace('_', ' ')}")
    
    # Create isolated vectorstore & engine for this specific user
    user_vectorstore = doc_manager.create_user_vectorstore(allowed_companies)
    
    if not user_vectorstore:
        st.warning("No documents found for your access level.")
    else:
        # Initialize Chat Engine
        chat_engine = ChatEngine(vectorstore=user_vectorstore, memory=st.session_state.memory)
        
        if chat_engine.is_mock_mode:
            st.info("💡 To enable real LLM responses, add `GOOGLE_API_KEY=your_key` to a `.env` file in this directory.")

        # Display Chat History
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle User Input
        if query := st.chat_input("Ask a question about your authorized documents..."):
            
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            # Generate and append assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_text = chat_engine.generate_response(query)
                    st.markdown(response_text)
                        
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

elif not st.session_state.logged_in_user:
    st.info("Please log in using the sidebar to access the Q&A system.")
