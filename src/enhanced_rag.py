import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.faiss_search import FAISSSearch
from src.config import GROQ_API_KEY, GROQ_MODEL
import groq

class EnhancedRAG:
    def __init__(self):
        self.searcher = FAISSSearch()
        self.client = None
        self.model_name = GROQ_MODEL
        self.setup_groq()
    
    def setup_groq(self):
        """Setup Groq client"""
        try:
            self.client = groq.Client(api_key=GROQ_API_KEY)
            print(f"✅ Groq client initialized with model: {self.model_name}")
        except Exception as e:
            print(f"❌ Failed to initialize Groq client: {e}")
    
    def get_context(self, query, k=5):
        """Get relevant context with better filtering"""
        results = self.searcher.search(query, k=k)
        if not results:
            return "No relevant information found."
        
        context_parts = []
        for i, result in enumerate(results):
            if result['score'] > 0.2:  # Only use reasonably relevant results
                source = result['metadata']['source']
                content = self.clean_content(result['content'])
                context_parts.append(f"DOCUMENT {i+1} [Source: {source}]:\n{content}")
        
        return "\n\n" + "="*50 + "\n".join(context_parts) + "\n" + "="*50
    
    def clean_content(self, content):
        """Clean and truncate content for better context"""
        # Remove excessive whitespace
        content = ' '.join(content.split())
        # Limit length
        if len(content) > 800:
            content = content[:800] + "..."
        return content
    
    def generate_answer(self, query, context):
        """Generate answer using Groq with better prompting"""
        if not self.client:
            return "Error: Groq client not available."
        
        prompt = f"""You are an AI legal assistant for Indian laws and government schemes. Use the provided context to answer the user's question.

Follow these rules:
1. Answer based ONLY on the provided context
2. If the context doesn't contain the answer, say "I cannot find specific information about this in the available documents."
3. Be precise and factual
4. If referring to laws, mention specific sections when possible
5. For schemes, mention eligibility and benefits when available

CONTEXT:{context}

USER QUESTION: {query}

ANSWER:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def ask(self, query, k=5):
        """Main method to ask questions"""
        print(f"🤔 Question: {query}")
        
        # Get relevant context
        context = self.get_context(query, k=k)
        relevant_sources = len(context.split("DOCUMENT")) - 1
        print(f"📚 Found {relevant_sources} relevant document(s)")
        
        if relevant_sources == 0:
            return "I couldn't find relevant information in my knowledge base about this topic."
        
        # Generate answer
        answer = self.generate_answer(query, context)
        return answer

def test_enhanced_rag():
    """Test the enhanced RAG pipeline"""
    print("🚀 Testing Enhanced RAG Pipeline...")
    print("=" * 60)
    
    rag = EnhancedRAG()
    
    test_questions = [
        "What is murder punishment in IPC?",
        "PM Kisan scheme eligibility",
        "Definition of theft",
        "Government schemes for farmers",
        "What is IPC Section 302?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"❓ Question: {question}")
        answer = rag.ask(question)
        print(f"🤖 Answer: {answer}")
        print(f"{'='*50}")

if __name__ == "__main__":
    test_enhanced_rag()