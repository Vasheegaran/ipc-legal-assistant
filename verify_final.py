import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def verify_final():
    """Final verification of Phase 2"""
    print("🎯 FINAL PHASE 2 VERIFICATION")
    print("=" * 50)
    
    # Test basic functionality
    try:
        from utils.file_handlers import load_documents
        docs = load_documents()
        print(f"✅ Document Loading: {len(docs)} documents")
        
        # Test if knowledge base exists and works
        kb_path = Path("knowledge_base/chroma_db")
        if kb_path.exists():
            print("✅ Knowledge Base: Directory exists")
            
            # Test search functionality
            try:
                from test_search import test_semantic_search
                test_semantic_search()
                print("✅ Semantic Search: Working!")
            except Exception as e:
                print(f"⚠️ Semantic Search: Needs building - {e}")
        else:
            print("❌ Knowledge Base: Not built yet")
            
    except Exception as e:
        print(f"❌ System check failed: {e}")
    
    print("=" * 50)
    print("📝 NEXT: If knowledge base builds successfully, we move to Phase 3!")
    print("💡 If there are issues, we'll use the minimal builder as backup.")

if __name__ == "__main__":
    verify_final()