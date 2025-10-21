import streamlit as st
import sys
from pathlib import Path
import os

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import with error handling
try:
    from src.enhanced_rag import EnhancedRAG
    RAG_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing RAG system: {e}")
    RAG_AVAILABLE = False

def main():
    st.set_page_config(
        page_title="⚖️ Indian Law & Policy Chatbot",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .user-message {
        background-color: #2b313e;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff4b4b;
    }
    .assistant-message {
        background-color: #1a1d29;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #00d4aa;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">⚖️ Indian Law & Policy Chatbot</div>', unsafe_allow_html=True)
    st.markdown("### Your AI Assistant for Indian Laws and Government Schemes")
    
    # Sidebar
    with st.sidebar:
        st.title("About")
        st.markdown("""
        **Capabilities:**
        - Indian Penal Code (IPC) sections
        - Government schemes & policies
        - Eligibility criteria
        - Legal definitions
        
        **Knowledge Base:**
        - 4 Legal Documents
        - FAISS Vector Search
        - Groq AI Powered
        
        *Always verify with official sources.*
        """)
        
        if st.button("Clear Chat History"):
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    
    # Initialize RAG system
    if RAG_AVAILABLE and "rag" not in st.session_state:
        with st.spinner("🔄 Loading AI Legal Assistant..."):
            try:
                st.session_state.rag = EnhancedRAG()
                st.success("✅ AI Assistant Ready!")
            except Exception as e:
                st.error(f"Failed to initialize AI: {e}")
                st.session_state.rag = None
    elif not RAG_AVAILABLE:
        st.error("❌ RAG system not available. Please check dependencies.")
        st.session_state.rag = None
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I'm your AI Legal Assistant. I can help you with questions about:\n\n• Indian Penal Code (IPC) sections\n• Government schemes like PM-KISAN\n• Legal definitions and punishments\n• Eligibility criteria\n\nWhat would you like to know?"
            }
        ]
    
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message"><strong>AI Assistant:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about Indian laws or policies..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        if st.session_state.rag:
            with st.spinner("🔍 Searching legal documents..."):
                try:
                    response = st.session_state.rag.ask(prompt)
                except Exception as e:
                    response = f"Error: {str(e)}"
        else:
            response = "AI system not available. Please check the setup."
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()