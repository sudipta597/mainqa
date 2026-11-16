from langchain_classic.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from utils.config import Config

class ChatEngine:
    """Manages the interactions with the LLM and the VectorStore retrieval."""
    
    def __init__(self, vectorstore: FAISS, memory):
        self.vectorstore = vectorstore
        self.memory = memory
        self.api_key = Config.GOOGLE_API_KEY
        self.is_mock_mode = not bool(self.api_key)
        
        self.qa_chain = None
        if not self.is_mock_mode:
            llm = ChatGoogleGenerativeAI(model=Config.LLM_MODEL, temperature=0)
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                memory=self.memory
            )

    def generate_response(self, query: str) -> str:
        """Generates a response either using an LLM or fallback mock retrieval."""
        if self.is_mock_mode:
            # Simple vector search returning top 2 chunks as context for testing RBAC
            docs = self.vectorstore.similarity_search(query, k=2)
            context = "\n\n---\n\n".join([doc.page_content for doc in docs])
            if not context:
                context = "No relevant context found."
            return f"**[MOCK MODE - NO API KEY]**\n\nRetrieved excerpts:\n\n{context}\n\n*(Add GOOGLE_API_KEY to your .env to enable the Generative LLM)*"
        else:
            # Real LLM Generation
            response = self.qa_chain.invoke({"question": query})
            return response['answer']
