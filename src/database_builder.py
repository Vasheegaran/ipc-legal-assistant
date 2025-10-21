import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def build_knowledge_base_v2():
    """Updated knowledge base builder for newer package versions"""
    print("🚀 Starting Knowledge Base Construction (v2)...")
    
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
        from utils.file_handlers import load_documents
        from src.config import (
            EMBEDDING_MODEL, 
            PERSIST_DIRECTORY, 
            CHUNK_SIZE, 
            CHUNK_OVERLAP
        )
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Trying alternative imports...")
        return build_knowledge_base_alternative()
    
    # Step 1: Load documents
    print("📂 Loading documents...")
    raw_documents = load_documents()
    
    if not raw_documents:
        print("❌ No documents found.")
        return
    
    print(f"📄 Loaded {len(raw_documents)} documents")
    
    # Convert to LangChain document format
    from langchain_core.documents import Document
    documents = []
    for doc in raw_documents:
        documents.append(Document(
            page_content=doc['content'],
            metadata={"source": doc['source'], "type": doc['type']}
        ))
    
    # Step 2: Split documents into chunks
    print("✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"📄 Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Step 3: Initialize embeddings model
    print("🔤 Loading embeddings model...")
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        print("✅ Embedding model loaded successfully!")
    except Exception as e:
        print(f"❌ Embedding model failed: {str(e)}")
        return None
    
    # Step 4: Create and persist vector store
    print("🗄️ Creating vector database...")
    
    try:
        # Clear existing database if it exists
        if os.path.exists(PERSIST_DIRECTORY):
            import shutil
            shutil.rmtree(PERSIST_DIRECTORY)
        
        # Create new vector store
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        
        print(f"✅ Knowledge base built successfully!")
        print(f"📍 Location: {PERSIST_DIRECTORY}")
        print(f"📊 Total chunks stored: {vector_store._collection.count()}")
        
        return vector_store
        
    except Exception as e:
        print(f"❌ Error creating vector database: {str(e)}")
        return None

def build_knowledge_base_alternative():
    """Alternative method using direct imports"""
    print("🔄 Trying alternative method...")
    
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import Chroma
        from utils.file_handlers import load_documents
        from src.config import PERSIST_DIRECTORY, CHUNK_SIZE, CHUNK_OVERLAP
        
        # Load documents
        raw_documents = load_documents()
        if not raw_documents:
            return None
            
        from langchain.schema import Document
        documents = []
        for doc in raw_documents:
            documents.append(Document(
                page_content=doc['content'],
                metadata={"source": doc['source'], "type": doc['type']}
            ))
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        print(f"📄 Created {len(chunks)} chunks")
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings()
        
        if os.path.exists(PERSIST_DIRECTORY):
            import shutil
            shutil.rmtree(PERSIST_DIRECTORY)
            
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        
        print(f"✅ Knowledge base built successfully (alternative)!")
        print(f"📍 Total chunks: {vector_store._collection.count()}")
        return vector_store
        
    except Exception as e:
        print(f"❌ Alternative method failed: {str(e)}")
        return None

if __name__ == "__main__":
    build_knowledge_base_v2()