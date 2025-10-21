import sys
from pathlib import Path
import pickle

sys.path.append(str(Path(__file__).parent))

def debug_system():
    """Debug the complete system"""
    print("🔧 DEBUGGING COMPLETE IPC SYSTEM")
    print("=" * 60)
    
    # Check 1: Knowledge base
    kb_path = Path("knowledge_base/ipc_complete")
    print(f"1. Knowledge base exists: {kb_path.exists()}")
    
    if kb_path.exists():
        files = list(kb_path.glob("*"))
        print(f"   Files: {[f.name for f in files]}")
        
        # Check metadata
        try:
            with open(kb_path / "metadata.pkl", 'rb') as f:
                data = pickle.load(f)
            print(f"   Sections in metadata: {data.get('section_count', 'Unknown')}")
        except Exception as e:
            print(f"   Metadata error: {e}")
    
    # Check 2: Try to import and initialize the RAG system
    print("\n2. Testing RAG system import...")
    try:
        from src.complete_ipc_rag import CompleteIPCRAG
        print("   ✅ CompleteIPCRAG import successful")
        
        # Try to initialize
        print("   🔄 Initializing RAG system...")
        rag = CompleteIPCRAG()
        print("   ✅ RAG system initialized")
        
        # Test a simple query
        print("   🔄 Testing query...")
        response = rag.ask("IPC Section 302")
        print(f"   ✅ Query response: {response[:100]}...")
        
    except Exception as e:
        print(f"   ❌ RAG system error: {e}")
        import traceback
        traceback.print_exc()
    
    # Check 3: Test FAISS directly
    print("\n3. Testing FAISS directly...")
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
        
        # Load the index
        index = faiss.read_index(str(kb_path / "index.faiss"))
        print("   ✅ FAISS index loaded")
        
        # Load metadata
        with open(kb_path / "metadata.pkl", 'rb') as f:
            data = pickle.load(f)
        
        # Test search
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_query = "murder punishment"
        query_embedding = model.encode([test_query])
        faiss.normalize_L2(query_embedding)
        D, I = index.search(query_embedding, k=3)
        
        print(f"   ✅ Search test successful")
        print(f"   Query: '{test_query}'")
        for i, idx in enumerate(I[0]):
            if idx < len(data['texts']):
                section_text = data['texts'][idx].split(" | ")[0]
                print(f"   Result {i+1}: {section_text}")
                
    except Exception as e:
        print(f"   ❌ FAISS test failed: {e}")

if __name__ == "__main__":
    debug_system()