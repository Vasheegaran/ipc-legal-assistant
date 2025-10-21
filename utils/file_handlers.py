import os
from PyPDF2 import PdfReader
from docx import Document
from typing import List, Dict, Any

def load_documents(data_dir: str = "data") -> List[Dict[str, Any]]:
    """
    Load all documents from the data directory and its subdirectories.
    Supports PDF, TXT, and DOCX files.
    """
    documents = []
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            
            try:
                if file_extension == '.pdf':
                    content = read_pdf(file_path)
                elif file_extension == '.txt':
                    content = read_txt(file_path)
                elif file_extension == '.docx':
                    content = read_docx(file_path)
                else:
                    print(f"Unsupported file format: {file_path}")
                    continue
                
                if content.strip():
                    documents.append({
                        'content': content,
                        'source': file_path,
                        'type': file_extension
                    })
                    print(f"✓ Loaded: {file_path}")
                else:
                    print(f"✗ Empty file: {file_path}")
                    
            except Exception as e:
                print(f"✗ Error loading {file_path}: {str(e)}")
    
    print(f"\n📊 Total documents loaded: {len(documents)}")
    return documents

def read_pdf(file_path: str) -> str:
    """Extract text from PDF files"""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {str(e)}")
    return text

def read_txt(file_path: str) -> str:
    """Read text from TXT files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def read_docx(file_path: str) -> str:
    """Extract text from DOCX files"""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {str(e)}")
    return text

if __name__ == "__main__":
    # Test the document loader
    test_docs = load_documents()
    print(f"Test loaded {len(test_docs)} documents")