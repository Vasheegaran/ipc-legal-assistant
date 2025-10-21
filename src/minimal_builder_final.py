import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def build_minimal_kb():
    """Minimal knowledge base builder that definitely works"""
    print("🚀 Starting Minimal Knowledge Base Construction...")
    
    try:
        from utils.file_handlers import load_documents
        from sentence_transformers import SentenceTransformer
        import chromadb
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return None
    
    # Step 1: Load documents
    print("📂 Loading documents...")
    raw_documents = load_documents()
    
    if not raw_documents:
        print("❌ No documents found.")
        return
    
    print(f"📄 Loaded {len(raw_documents)} documents")
    
    # Step 2: Initialize embeddings model
    print("🔤 Loading embeddings model...")
    try:
        # Use the model we already downloaded
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Step 3: Create ChromaDB client
    print("🗄️ Creating vector database...")
    try:
        client = chromadb.PersistentClient(path="knowledge_base/chroma_db")
        
        # Delete existing collection if it exists
        try:
            client.delete_collection("legal_docs")
            print("♻️  Deleted existing collection")
        except:
            pass
            
        collection = client.get_or_create_collection(
            name="legal_docs",
            metadata={"description": "Indian Legal Documents and Policies"}
        )
        
        # Process documents and create chunks
        print("✂️ Processing documents into chunks...")
        all_texts = []
        all_metadatas = []
        all_ids = []
        
        chunk_id = 0
        for doc_idx, doc in enumerate(raw_documents):
            # Simple chunking - split by paragraphs and sentences
            content = doc['content']
            
            # Split into paragraphs
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            for para_idx, paragraph in enumerate(paragraphs):
                if len(paragraph) > 100:  # Only include substantial paragraphs
                    all_texts.append(paragraph)
                    all_metadatas.append({
                        "source": os.path.basename(doc['source']),
                        "doc_index": doc_idx,
                        "chunk_index": para_idx,
                        "type": doc['type'],
                        "full_source": doc['source']
                    })
                    all_ids.append(f"chunk_{chunk_id}")
                    chunk_id += 1
        
        print(f"📦 Created {len(all_texts)} chunks from documents")
        
        # Process in smaller batches to avoid memory issues
        batch_size = 50
        total_batches = (len(all_texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(all_texts), batch_size):
            batch_texts = all_texts[i:i + batch_size]
            batch_metadatas = all_metadatas[i:i + batch_size]
            batch_ids = all_ids[i:i + batch_size]
            
            print(f"🔄 Processing batch {i//batch_size + 1}/{total_batches}...")
            
            # Generate embeddings for this batch
            embeddings = model.encode(batch_texts).tolist()
            
            # Add to collection
            collection.add(
                embeddings=embeddings,
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        
        print(f"✅ Knowledge base built successfully!")
        print(f"📍 Location: knowledge_base/chroma_db")
        print(f"📊 Total chunks stored: {collection.count()}")
        
        # Test the collection
        print("\n🧪 Testing collection...")
        test_results = collection.query(
            query_texts=["What is punishment for murder?"],
            n_results=2
        )
        
        if test_results['documents']:
            print("✅ Collection test successful!")
            for i, doc in enumerate(test_results['documents'][0]):
                print(f"   Sample result {i+1}: {doc[:100]}...")
        else:
            print("⚠️ Collection test returned no results")
        
        return collection
        
    except Exception as e:
        print(f"❌ Error building knowledge base: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    build_minimal_kb()