import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="⚖️ Simple IPC Chatbot",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("⚖️ Simple IPC Chatbot")
    st.markdown("### Ask about any IPC Section (1-575)")
    
    # Initialize simple RAG
    if "simple_rag" not in st.session_state:
        with st.spinner("🔄 Loading IPC Database..."):
            try:
                from src.complete_ipc_rag import CompleteIPCRAG
                st.session_state.simple_rag = CompleteIPCRAG()
                st.success("✅ IPC System Ready!")
            except Exception as e:
                st.error(f"❌ System load failed: {e}")
                st.session_state.simple_rag = None
    
    # Quick section buttons
    st.markdown("**Quick Sections:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("§302 - Murder"):
            st.session_state.query = "IPC Section 302 punishment for murder"
    with col2:
        if st.button("§375 - Rape Def"):
            st.session_state.query = "IPC Section 375 definition of rape"
    with col3:
        if st.button("§511 - Attempts"):
            st.session_state.query = "Explain Section 511 about attempts"
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me about any IPC section (1-575)!"}
        ]
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle input
    query = st.chat_input("Ask about IPC sections...")
    if "query" in st.session_state:
        query = st.session_state.query
        st.session_state.query = None
    
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching IPC..."):
                if st.session_state.simple_rag:
                    response = st.session_state.simple_rag.ask(query)
                else:
                    response = "System not available"
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()