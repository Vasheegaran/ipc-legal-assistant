import os
import sys
import pickle
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def build_faiss_knowledge_base():
    """Build knowledge base using FAISS instead of ChromaDB"""
    print("🚀 Starting FAISS Knowledge Base Construction...")
    
    try:
        from utils.file_handlers import load_documents
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np
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
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Step 3: Create chunks from documents
    print("✂️ Creating document chunks...")
    all_texts = []
    all_metadatas = []
    
    for doc_idx, doc in enumerate(raw_documents):
        content = doc['content']
        
        # Simple chunking - split by paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
        
        for para_idx, paragraph in enumerate(paragraphs):
            all_texts.append(paragraph)
            all_metadatas.append({
                "source": os.path.basename(doc['source']),
                "doc_index": doc_idx,
                "chunk_index": para_idx,
                "type": doc['type'],
                "full_source": doc['source']
            })
    
    print(f"📦 Created {len(all_texts)} chunks from documents")
    
    if not all_texts:
        print("❌ No valid chunks created!")
        return
    
    # Step 4: Generate embeddings
    print("🧮 Generating embeddings...")
    embeddings = model.encode(all_texts)
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # Step 5: Create FAISS index
    print("🗄️ Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    # Step 6: Save everything
    print("💾 Saving knowledge base...")
    kb_dir = Path("knowledge_base/faiss_db")
    kb_dir.mkdir(parents=True, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(index, str(kb_dir / "index.faiss"))
    
    # Save metadata and texts
    with open(kb_dir / "metadata.pkl", 'wb') as f:
        pickle.dump({
            'texts': all_texts,
            'metadatas': all_metadatas,
            'dimension': dimension
        }, f)
    
    print(f"✅ FAISS knowledge base built successfully!")
    print(f"📍 Location: {kb_dir}")
    print(f"📊 Total chunks stored: {len(all_texts)}")
    
    # Test the index
    print("\n🧪 Testing FAISS index...")
    test_query = "What is punishment for murder?"
    test_embedding = model.encode([test_query])
    faiss.normalize_L2(test_embedding)
    
    D, I = index.search(test_embedding, k=3)
    
    if len(I[0]) > 0:
        print("✅ FAISS test successful!")
        for i, idx in enumerate(I[0]):
            if idx < len(all_texts):
                print(f"   Result {i+1}: {all_texts[idx][:100]}...")
    else:
        print("⚠️ FAISS test returned no results")
    
    return {
        'index': index,
        'texts': all_texts,
        'metadatas': all_metadatas,
        'model': model
    }

if __name__ == "__main__":
    build_faiss_knowledge_base()