import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="⚖️ IPC Legal Assistant",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("⚖️ Indian Penal Code Chatbot")
    st.markdown("### Ask about any IPC Section (1-575)")
    
    # Initialize RAG
    if "rag" not in st.session_state:
        with st.spinner("🔄 Loading IPC Database (575 Sections)..."):
            try:
                from src.complete_ipc_rag import CompleteIPCRAG
                st.session_state.rag = CompleteIPCRAG()
                st.success("✅ IPC System Ready!")
            except Exception as e:
                st.error(f"❌ System load failed: {e}")
                st.session_state.rag = None
    
    # Quick access buttons
    st.markdown("**Quick Access:**")
    cols = st.columns(4)
    with cols[0]:
        if st.button("§302 Murder"):
            st.session_state.user_input = "What is IPC Section 302 punishment for murder?"
    with cols[1]:
        if st.button("§375 Rape"):
            st.session_state.user_input = "Explain IPC Section 375 definition of rape"
    with cols[2]:
        if st.button("§511 Attempts"):
            st.session_state.user_input = "Explain Section 511 about attempts to commit offences"
    with cols[3]:
        if st.button("§420 Cheating"):
            st.session_state.user_input = "What is IPC Section 420 punishment for cheating?"
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I can help you with any IPC section from 1 to 575. Ask me about legal definitions, punishments, or specific sections!"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Get user input
    if "user_input" in st.session_state:
        user_input = st.session_state.user_input
        del st.session_state.user_input
    else:
        user_input = st.chat_input("Ask about IPC sections...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.chat_message("assistant"):
            if st.session_state.rag:
                with st.spinner("🔍 Searching IPC database..."):
                    response = st.session_state.rag.ask(user_input)
            else:
                response = "System not available. Please refresh the page."
            
            st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the chat
        st.rerun()

if __name__ == "__main__":
    main()