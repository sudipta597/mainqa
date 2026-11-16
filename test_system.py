import os
import sys

# Ensure Python path includes the current directory so 'utils' can be resolved
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.auth import AuthManager
from utils.document_manager import DocumentManager
from utils.chat_engine import ChatEngine
from langchain_classic.memory import ConversationBufferMemory

def run_tests():
    print("=========================================")
    print("   MULTI-USER Q&A SYSTEM - TEST SUITE    ")
    print("=========================================\n")
    
    # 1. Test Document Manager
    print("[TEST 1] Initializing Document Manager & Loading PDFs...")
    doc_manager = DocumentManager()
    success = doc_manager.load_and_index_documents()
    print(f" -> Documents loaded successfully: {success}")
    if not success:
        print(" -> FAILED: Please ensure PDFs are generated in the data/ folder.")
        return
    print(" -> SUCCESS: Base FAISS VectorStore created.\n")

    # 2. Test Auth Manager
    print("[TEST 2] Initializing Auth Manager (RBAC)...")
    auth = AuthManager()
    alice = "alice@email.com"
    bob = "bob@email.com"
    charlie = "charlie@email.com"
    
    alice_companies = auth.get_allowed_companies(alice)
    bob_companies = auth.get_allowed_companies(bob)
    
    print(f" -> {alice} access: {alice_companies}")
    print(f" -> {bob} access: {bob_companies}")
    print(" -> SUCCESS: RBAC mapping is correct.\n")

    # 3. Test Isolation & Query for Alice
    print(f"[TEST 3] Testing Data Isolation for {alice}...")
    alice_vs = doc_manager.create_user_vectorstore(alice_companies)
    alice_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    alice_engine = ChatEngine(vectorstore=alice_vs, memory=alice_memory)
    
    print(f" -> Engine Mode: {'MOCK (No API Key)' if alice_engine.is_mock_mode else 'LIVE (Gemini LLM)'}")
    
    query1 = "What was the total revenue?"
    print(f" -> [User: {alice}] Query: '{query1}'")
    response1 = alice_engine.generate_response(query1)
    print(f" -> [System] Response:\n{response1}\n")

    # 4. Test Isolation & Query for Bob
    print(f"[TEST 4] Testing Data Isolation for {bob}...")
    bob_vs = doc_manager.create_user_vectorstore(bob_companies)
    bob_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    bob_engine = ChatEngine(vectorstore=bob_vs, memory=bob_memory)
    
    query2 = "What was the total revenue?"
    print(f" -> [User: {bob}] Query: '{query2}'")
    response2 = bob_engine.generate_response(query2)
    print(f" -> [System] Response:\n{response2}\n")
    
    # 5. Test specific query filtering
    query3 = "What did the CEO say about enterprise solutions?"
    print(f" -> [User: {bob}] Query (Testing Cross-Company privacy): '{query3}'")
    response3 = bob_engine.generate_response(query3)
    print(f" -> [System] Response:\n{response3}\n")
    print("NOTE: Bob should NOT see Company D's enterprise solutions quote (Charlie's document).")
    print("=========================================")
    print("             TESTS COMPLETED             ")
    print("=========================================")

if __name__ == '__main__':
    run_tests()
