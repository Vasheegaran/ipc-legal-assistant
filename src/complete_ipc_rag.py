import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

class CompleteIPCRAG:
    def __init__(self):
        self.searcher = None
        self.client = None
        self.model_name = "llama-3.1-8b-instant"
        self.setup_components()
    
    def setup_components(self):
        """Setup all components for complete IPC coverage"""
        print("🔄 Initializing Complete IPC Legal Assistant...")
        
        # Setup Groq client
        try:
            import groq
            from src.config import GROQ_API_KEY
            self.client = groq.Client(api_key=GROQ_API_KEY)
            print("✅ Groq client initialized")
        except Exception as e:
            print(f"❌ Groq setup failed: {e}")
            self.client = None
        
        # Setup FAISS search with complete IPC knowledge base
        try:
            # First try enhanced IPC knowledge base
            from src.faiss_search import FAISSSearch
            self.searcher = FAISSSearch()
            
            # Try multiple knowledge base paths
            knowledge_bases = [
                "knowledge_base/ipc_complete",
                "knowledge_base/faiss_db",  # fallback
            ]
            
            loaded = False
            for kb_path in knowledge_bases:
                if self.searcher.load_knowledge_base(kb_path):
                    print(f"✅ Knowledge base loaded from: {kb_path}")
                    loaded = True
                    break
            
            if not loaded:
                print("❌ No knowledge base could be loaded")
                self.searcher = None
                
        except Exception as e:
            print(f"❌ FAISS setup failed: {e}")
            self.searcher = None
    
    def get_ipc_context(self, query, k=5):
        """Get comprehensive IPC context"""
        if not self.searcher:
            return "IPC legal database not available."
        
        results = self.searcher.search(query, k=k)
        if not results:
            return "No relevant IPC sections found."
        
        context_parts = []
        for i, result in enumerate(results):
            if result['score'] > 0.1:  # Lower threshold for comprehensive coverage
                metadata = result['metadata']
                content = self.format_ipc_content(result['content'], metadata)
                context_parts.append(content)
        
        if not context_parts:
            return "No sufficiently relevant IPC sections found."
        
        return "\n\n" + "="*60 + "\n" + "\n".join(context_parts) + "\n" + "="*60
    
    def format_ipc_content(self, content, metadata):
        """Format IPC content for better readability"""
        section_num = metadata.get('section', 'N/A')
        section_title = metadata.get('section_title', '')
        chapter = metadata.get('chapter', '')
        chapter_title = metadata.get('chapter_title', '')
        
        formatted = f"⚖️ IPC Section {section_num}: {section_title}\n"
        if chapter and chapter_title:
            formatted += f"📖 Chapter {chapter}: {chapter_title}\n"
        
        # Extract the main description from content
        content_lines = content.split(" | ")
        for line in content_lines:
            if line.startswith("Description:") or line.startswith("Legal Provision:"):
                formatted += f"📝 {line}\n"
                break
        
        return formatted
    
    def generate_ipc_answer(self, query, context):
        """Generate comprehensive IPC answer"""
        if not self.client:
            return "IPC legal information service temporarily unavailable."
        
        prompt = f"""You are an expert Indian Penal Code (IPC) legal assistant.
Provide accurate, comprehensive legal information based ONLY on the provided IPC context.

RULES:
1. Answer based ONLY on the provided IPC context
2. Be precise about sections, punishments, definitions
3. Mention relevant chapter information when available
4. If context doesn't contain the specific section, say "This specific IPC section is not available in my current database."
5. Always cite the exact section numbers

IPC CONTEXT:{context}

LEGAL QUESTION: {query}

COMPREHENSIVE IPC ANSWER:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Legal information service error: {str(e)}"
    
    def ask(self, query):
        """Main method to ask IPC questions"""
        print(f"⚖️ IPC Query: {query}")
        
        # Check if components are available
        if not self.searcher or not self.client:
            return "Complete IPC system not available. Please check if the knowledge base is properly loaded."
        
        # Use comprehensive IPC approach
        context = self.get_ipc_context(query, k=5)
        
        if "No relevant IPC sections" in context or "not available" in context:
            return "I couldn't find relevant IPC sections for your query. Please try asking about specific IPC sections or crimes."
        
        print(f"📚 Found relevant context")
        answer = self.generate_ipc_answer(query, context)
        return answer

def test_complete_ipc():
    """Test the complete IPC RAG system"""
    print("⚖️ Testing Complete IPC RAG System")
    print("=" * 70)
    
    rag = CompleteIPCRAG()
    
    # Test various IPC queries
    test_questions = [
        "What is IPC Section 302?",
        "Punishment for murder",
        "Section 511 about attempts",
        "Explain rape laws in IPC"
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"❓ Question: {question}")
        answer = rag.ask(question)
        print(f"🤖 Answer: {answer}")
        print(f"{'='*60}")

if __name__ == "__main__":
    test_complete_ipc()