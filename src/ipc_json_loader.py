import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def create_ipc_knowledge_base():
    """Create IPC knowledge base from JSON - CLEAN VERSION"""
    print("📚 Creating IPC Knowledge Base from JSON...")
    
    try:
        # Load IPC JSON data
        json_path = Path("data/ipc/ipc_sections.json")
        if not json_path.exists():
            print("❌ IPC JSON file not found at:", json_path)
            return False
            
        with open(json_path, 'r', encoding='utf-8') as f:
            ipc_data = json.load(f)
        
        print(f"📖 Loaded {len(ipc_data)} IPC sections")
        
        # Create text chunks for each section
        all_texts = []
        all_metadatas = []
        
        for section in ipc_data:
            # Create comprehensive text for better search
            text = (
                f"IPC Section {section['Section']} | "
                f"Title: {section['section_title']} | "
                f"Description: {section['section_desc']} | "
                f"Chapter {section['chapter']}: {section['chapter_title']}"
            )
            all_texts.append(text)
            
            all_metadatas.append({
                "source": "Indian Penal Code",
                "section": section['Section'],
                "section_title": section['section_title'],
                "chapter": section['chapter'],
                "chapter_title": section['chapter_title'],
                "type": "ipc_section"
            })
        
        print(f"📦 Created {len(all_texts)} section entries")
        
        # Create embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(all_texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        
        # Save knowledge base
        kb_dir = Path("knowledge_base/ipc_complete")
        kb_dir.mkdir(parents=True, exist_ok=True)
        
        faiss.write_index(index, str(kb_dir / "index.faiss"))
        with open(kb_dir / "metadata.pkl", 'wb') as f:
            pickle.dump({
                'texts': all_texts,
                'metadatas': all_metadatas,
                'dimension': dimension,
                'section_count': len(all_texts)
            }, f)
        
        print(f"✅ IPC Knowledge Base saved successfully!")
        print(f"📍 Location: {kb_dir}")
        print(f"📊 Total sections: {len(all_texts)}")
        
        # Simple test to verify it works
        print("\n🧪 Quick verification:")
        test_embedding = model.encode(["murder punishment"])
        faiss.normalize_L2(test_embedding)
        D, I = index.search(test_embedding, k=1)
        
        if len(I[0]) > 0:
            found_section = all_texts[I[0][0]].split(" | ")[0]
            print(f"   Test query 'murder punishment' → {found_section}")
        else:
            print("   Test query returned no results")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_ipc_knowledge_base()
    if success:
        print("\n🎉 SUCCESS! IPC Knowledge Base created.")
        print("🚀 Now run: streamlit run app_complete_ipc.py")
    else:
        print("\n💡 Please check your setup and try again.")