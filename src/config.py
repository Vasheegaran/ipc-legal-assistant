import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Groq API Configuration - Updated models
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # Updated model - fast and free
# Alternative models you can use:
# "llama-3.1-70b-versatile" - More powerful but slower
# "mixtral-8x7b-32768" - Good balance of speed and quality

# Embeddings Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# FAISS Configuration
FAISS_DIRECTORY = "knowledge_base/faiss_db"

# Document Processing Configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Supported Document Formats
SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.docx']