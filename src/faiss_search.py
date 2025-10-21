import sys
from pathlib import Path
import pickle

sys.path.append(str(Path(__file__).parent.parent))

class FAISSSearch:
    def __init__(self):
        self.index = None
        self.texts = None
        self.metadatas = None
        self.model = None
        self.loaded = False
        
    def load_knowledge_base(self, kb_path=None):
        """Load the FAISS knowledge base with optional path"""
        try:
            import faiss
            from sentence_transformers import SentenceTransformer
            
            if kb_path is None:
                kb_path = "knowledge_base/faiss_db"
            
            kb_dir = Path(kb_path)
            if not kb_dir.exists():
                print(f"❌ Knowledge base not found at: {kb_path}")
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(str(kb_dir / "index.faiss"))
            
            # Load metadata and texts
            with open(kb_dir / "metadata.pkl", 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.metadatas = data['metadatas']
            
            # Load model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.loaded = True
            print(f"✅ Knowledge base loaded from: {kb_path}")
            print(f"   Sections available: {len(self.texts)}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load knowledge base from {kb_path}: {e}")
            return False
    
    def search(self, query, k=3):
        """Search the knowledge base"""
        if not self.loaded:
            if not self.load_knowledge_base():
                return []
        
        try:
            import faiss
            import numpy as np
            
            # Encode query
            query_embedding = self.model.encode([query])
            
            # Normalize for cosine similarity
            faiss.normalize_L2(query_embedding)
            
            # Search
            D, I = self.index.search(query_embedding, k=k)
            
            results = []
            for i, idx in enumerate(I[0]):
                if idx < len(self.texts):
                    results.append({
                        'content': self.texts[idx],
                        'metadata': self.metadatas[idx],
                        'score': D[0][i]
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []

def test_faiss_search():
    """Test FAISS search functionality"""
    print("🔍 Testing FAISS Search...")
    
    searcher = FAISSSearch()
    
    # Try to load IPC knowledge base
    if searcher.load_knowledge_base("knowledge_base/ipc_complete"):
        test_queries = [
            "punishment for murder",
            "section 511 attempts",
            "rape definition"
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            results = searcher.search(query, k=2)
            
            if results:
                for i, result in enumerate(results):
                    print(f"📄 Result {i+1} (score: {result['score']:.3f}):")
                    print(f"   Content: {result['content'][:150]}...")
                    print(f"   Section: {result['metadata'].get('section', 'N/A')}")
                    print("   ---")
            else:
                print("   No results found")
    else:
        print("❌ Could not load knowledge base")

if __name__ == "__main__":
    test_faiss_search()