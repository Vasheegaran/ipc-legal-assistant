import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="⚖️ Complete IPC Chatbot - All 511 Sections",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS for IPC chatbot
    st.markdown("""
    <style>
    .ipc-header {
        font-size: 3rem;
        color: #0d47a1;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        background: linear-gradient(45deg, #0d47a1, #1976d2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-button {
        background-color: #e3f2fd;
        color: #1565c0;
        border: 2px solid #bbdefb;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    .section-button:hover {
        background-color: #bbdefb;
        border-color: #64b5f6;
        transform: translateY(-2px);
    }
    .quick-access {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="ipc-header">⚖️ Complete IPC Chatbot</div>', unsafe_allow_html=True)
    st.markdown("### 📚 All 511 Sections of Indian Penal Code")
    
    # Sidebar with IPC Chapter Navigation
    with st.sidebar:
        st.title("📖 IPC Chapters")
        
        # IPC Chapters quick navigation
        ipc_chapters = {
            "1-5": "Introduction & General Explanations",
            "6-15": "Of Punishments",
            "16-21": "Offences Against Human Body", 
            "22-27": "Offences Against Property",
            "28-31": "Criminal Breach of Contracts",
            "32-40": "Offences Relating to Documents",
            "41-60": "Criminal Intimidation & More"
        }
        
        st.markdown("**Quick Chapter Access:**")
        for chapter_range, title in ipc_chapters.items():
            if st.button(f"Ch {chapter_range}: {title}"):
                st.session_state.last_query = f"IPC Chapter {chapter_range} {title}"
        
        st.markdown("---")
        st.markdown("**🔍 Common Sections:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("§302 Murder"):
                st.session_state.last_query = "IPC Section 302 punishment for murder"
            if st.button("§375 Rape Def"):
                st.session_state.last_query = "IPC Section 375 definition of rape"
            if st.button("§420 Cheating"):
                st.session_state.last_query = "IPC Section 420 cheating punishment"
        with col2:
            if st.button("§376 Rape Pun"):
                st.session_state.last_query = "IPC Section 376 punishment for rape"
            if st.button("§379 Theft"):
                st.session_state.last_query = "IPC Section 379 theft"
            if st.button("§511 Attempts"):
                st.session_state.last_query = "IPC Section 511 attempts to commit offences"
        
        st.markdown("---")
        st.markdown("**ℹ️ About:**")
        st.markdown("""
        - **511 IPC Sections**
        - **Complete Coverage**
        - **Legal Expert AI**
        - **Instant Responses**
        """)
        
        if st.button("🔄 Clear Chat"):
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()
    
    # Quick Section Access
    st.markdown('<div class="quick-access">', unsafe_allow_html=True)
    st.markdown("### 🚀 Quick Section Access")
    
    # Popular sections in columns
    popular_sections = [
        ("302", "Murder"), ("375", "Rape Def"), ("376", "Rape Pun"), 
        ("420", "Cheating"), ("379", "Theft"), ("499", "Defamation"),
        ("511", "Attempts"), ("304", "Culpable Homicide"), ("354", "Assault")
    ]
    
    cols = st.columns(3)
    for i, (section, title) in enumerate(popular_sections):
        with cols[i % 3]:
            if st.button(f"§{section} - {title}", key=f"sec_{section}"):
                st.session_state.last_query = f"IPC Section {section} {title}"
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize Complete IPC RAG
    if "complete_ipc_rag" not in st.session_state:
        with st.spinner("🔄 Loading Complete IPC Database (511 Sections)..."):
            try:
                from src.complete_ipc_rag import CompleteIPCRAG
                st.session_state.complete_ipc_rag = CompleteIPCRAG()
                st.success("✅ Complete IPC AI Ready! (Sections 1-511)")
            except Exception as e:
                st.error(f"Complete IPC system load failed: {e}")
                st.session_state.complete_ipc_rag = None
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": """🎉 **Welcome to the Complete IPC Chatbot!**

I now have **complete coverage of all 511 sections** of the Indian Penal Code! 

**What I can help with:**
• Any IPC section from 1 to 511
• Legal definitions and punishments  
• Chapter-wise explanations
• Comparative analysis of sections

**Try asking:**
- "What is IPC Section 302?"
- "Punishment for rape under IPC"  
- "Definition of theft in Section 379"
- "Explain Section 511 about attempts"

Ask me about **any IPC section**!"""
            }
        ]
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle queries
    if "last_query" in st.session_state and st.session_state.last_query:
        query = st.session_state.last_query
        st.session_state.last_query = None
    else:
        query = st.chat_input("Ask about any IPC section (1-511)...")
    
    if query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Generate response
        if st.session_state.complete_ipc_rag:
            with st.spinner("🔍 Searching complete IPC database..."):
                try:
                    response = st.session_state.complete_ipc_rag.ask(query)
                except Exception as e:
                    response = f"System error: {str(e)}"
        else:
            response = "Complete IPC system not available."
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()