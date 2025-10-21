import streamlit as st
import sys
from pathlib import Path
import os

# Set Groq API key for Streamlit Cloud
os.environ['GROQ_API_KEY'] = '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'

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="⚖️ IPC Legal Assistant",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("⚖️ Indian Penal Code Chatbot")
    st.markdown("### Ask about any IPC Section (1-575)")
    
    # Initialize RAG with caching
    @st.cache_resource
    def load_rag_system():
        try:
            from src.complete_ipc_rag import CompleteIPCRAG
            rag = CompleteIPCRAG()
            return rag
        except Exception as e:
            st.error(f"Failed to load IPC system: {e}")
            return None
    
    # Load RAG system
    if "rag" not in st.session_state:
        with st.spinner("🔄 Loading IPC Database (575 Sections)..."):
            st.session_state.rag = load_rag_system()
            if st.session_state.rag:
                st.success("✅ IPC System Ready!")
    
    # Quick access buttons
    st.markdown("**Quick Access:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("§302 Murder"):
            st.session_state.user_input = "What is IPC Section 302 punishment for murder?"
    with col2:
        if st.button("§375 Rape"):
            st.session_state.user_input = "Explain IPC Section 375 definition of rape"
    with col3:
        if st.button("§511 Attempts"):
            st.session_state.user_input = "Explain Section 511 about attempts to commit offences"
    with col4:
        if st.button("§420 Cheating"):
            st.session_state.user_input = "What is IPC Section 420 punishment for cheating?"
    
    # Additional quick buttons
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("🔪 Murder"):
            st.session_state.user_input = "punishment for murder"
    with col6:
        if st.button("🚫 Rape"):
            st.session_state.user_input = "rape laws punishment"
    with col7:
        if st.button("💰 Theft"):
            st.session_state.user_input = "theft definition and punishment"
    with col8:
        if st.button("🤥 Cheating"):
            st.session_state.user_input = "cheating section 420"
    
    st.markdown("---")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": """
                **Hello! I'm your AI Legal Assistant** 🤖⚖️
                
                I can help you with:
                • **Any IPC section** from 1 to 575
                • **Legal definitions** and punishments
                • **Crime-specific** information
                • **Chapter-wise** explanations
                
                **Try asking:**
                - "What is punishment for murder?"
                - "Explain Section 511 about attempts"
                - "Rape laws in IPC"
                - "Define theft"
                - "Section 420 cheating"
                """
            }
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if "user_input" in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input
    else:
        user_input = st.chat_input("Ask about IPC sections (1-575)...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            if st.session_state.rag:
                with st.spinner("🔍 Searching IPC database..."):
                    try:
                        response = st.session_state.rag.ask(user_input)
                    except Exception as e:
                        response = f"Error: {str(e)}"
            else:
                response = "❌ IPC system not available. Please refresh the page."
            
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()