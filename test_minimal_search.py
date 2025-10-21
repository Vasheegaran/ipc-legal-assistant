import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def test_minimal_search():
    """Test semantic search using minimal approach"""
    print("🔍 Testing Minimal Semantic Search...")
    
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        
        # Load model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded")
        
        # Connect to ChromaDB
        client = chromadb.PersistentClient(path="knowledge_base/chroma_db")
        collection = client.get_collection("legal_docs")
        print("✅ ChromaDB connected")
        
        # Test queries
        test_queries = [
            "What is punishment for murder?",
            "Who is eligible for PM Kisan scheme?",
            "What is the definition of theft?",
            "Government schemes for farmers"
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            
            # Generate query embedding
            query_embedding = model.encode([query]).tolist()
            
            # Search
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=3
            )
            
            if results['documents']:
                for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                    print(f"📄 Result {i+1}:")
                    print(f"   Content: {doc[:150]}...")
                    print(f"   Source: {metadata['source']}")
                    print("   ---")
            else:
                print("   No results found")
                
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_minimal_search()