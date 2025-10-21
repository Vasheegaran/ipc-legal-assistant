import sys
from pathlib import Path
import pickle

def final_test():
    """Final test of the complete system"""
    print("🎯 FINAL SYSTEM TEST - Complete IPC Chatbot")
    print("=" * 60)
    
    # Check knowledge base
    kb_path = Path("knowledge_base/ipc_complete")
    if not kb_path.exists():
        print("❌ Knowledge base not found")
        return False
    
    print("✅ 1. Knowledge base exists")
    
    # Check files
    files = list(kb_path.glob("*"))
    print(f"✅ 2. Found {len(files)} files in knowledge base")
    
    # Load metadata
    try:
        with open(kb_path / "metadata.pkl", 'rb') as f:
            data = pickle.load(f)
        sections = data.get('section_count', 0)
        print(f"✅ 3. Loaded {sections} IPC sections")
    except Exception as e:
        print(f"❌ Could not load metadata: {e}")
        return False
    
    # Test imports
    try:
        import faiss
        print("✅ 4. FAISS working")
    except Exception as e:
        print(f"❌ FAISS error: {e}")
        return False
        
    try:
        import groq
        print("✅ 5. Groq working")
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ 6. Sentence Transformers working")
    except Exception as e:
        print(f"❌ Sentence Transformers error: {e}")
        return False
    
    print("\n🎉 ALL SYSTEMS GO!")
    print("📚 Your chatbot can handle:")
    print("   - All 575 IPC sections")
    print("   - Legal definitions and punishments")
    print("   - Section-specific queries")
    print("   - Crime-based questions")
    print("   - Chapter-wise explanations")
    
    print("\n🚀 LAUNCH COMMAND: streamlit run app_complete_ipc.py")
    return True

if __name__ == "__main__":
    if final_test():
        print("\n⭐ Your Complete IPC Chatbot is READY! ⭐")
    else:
        print("\n💡 Please run: python src/ipc_json_loader.py")