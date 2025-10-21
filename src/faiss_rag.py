import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.faiss_search import FAISSSearch
from src.config import GROQ_API_KEY, GROQ_MODEL
import groq

class FAISSRAG:
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
    
    def get_context(self, query, k=3):
        """Get relevant context for query"""
        results = self.searcher.search(query, k=k)
        if not results:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        for i, result in enumerate(results):
            source = result['metadata']['source']
            content = result['content'][:500]  # Limit context length
            context_parts.append(f"Source: {source}\nContent: {content}")
        
        return "\n\n".join(context_parts)
    
    def generate_answer(self, query, context):
        """Generate answer using Groq"""
        if not self.client:
            return "Error: Groq client not available. Please check your API key."
        
        prompt = f"""You are a helpful legal assistant for Indian laws and government schemes. 
Answer the user's question based ONLY on the provided context from official documents. 
If the context doesn't contain the answer, say "I don't have enough information about this in my knowledge base."

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a precise legal assistant that provides accurate information about Indian laws and government schemes. Only use information from the provided context. If the context doesn't contain the answer, clearly state this."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def ask(self, query, k=3):
        """Main method to ask questions"""
        print(f"🤔 Question: {query}")
        
        # Get relevant context
        context = self.get_context(query, k=k)
        print(f"📚 Found relevant context from {len(context.split('Source:')) - 1} sources")
        
        # Generate answer
        answer = self.generate_answer(query, context)
        return answer

def test_rag():
    """Test the RAG pipeline"""
    print("🧪 Testing FAISS RAG Pipeline with Updated Model...")
    print("=" * 60)
    
    rag = FAISSRAG()
    
    test_questions = [
        "What is the punishment for murder under IPC?",
        "Who can apply for PM Kisan scheme?",
        "What constitutes theft according to Indian law?",
        "What are the eligibility criteria for government schemes?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"❓ Question: {question}")
        answer = rag.ask(question)
        print(f"🤖 Answer: {answer}")
        print(f"{'='*50}")

if __name__ == "__main__":
    test_rag()