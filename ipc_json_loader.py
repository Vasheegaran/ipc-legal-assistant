import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle

class IPCKnowledgeBase:
    def __init__(self):
        self.sections = []
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        
    def load_ipc_data(self, json_file):
        """Load IPC data from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.sections = []
            for section in data.get('sections', []):
                section_text = f"IPC Section {section['section']}: {section['title']}. {section['description']} Punishment: {section['punishment']}"
                self.sections.append({
                    'section': section['section'],
                    'title': section['title'],
                    'description': section['description'],
                    'punishment': section['punishment'],
                    'chapter': section.get('chapter', ''),
                    'full_text': section_text
                })
            
            print(f"📖 Loaded {len(self.sections)} IPC sections")
            return self.sections
        except Exception as e:
            print(f"❌ Error loading IPC data: {e}")
            return []
    
    def create_embeddings(self):
        """Create embeddings for all sections"""
        if not self.sections:
            print("❌ No sections loaded. Please load IPC data first.")
            return False
            
        texts = [section['full_text'] for section in self.sections]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        print(f"✅ Created embeddings for {len(texts)} sections")
        return True
    
    def save_knowledge_base(self, save_path):
        """Save knowledge base to disk"""
        try:
            os.makedirs(save_path, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, os.path.join(save_path, 'ipc_complete.index'))
            
            # Save sections data
            with open(os.path.join(save_path, 'ipc_complete.pkl'), 'wb') as f:
                pickle.dump(self.sections, f)
            
            print(f"✅ Knowledge base saved to {save_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
            return False
    
    def load_knowledge_base(self, save_path):
        """Load knowledge base from disk"""
        try:
            if not os.path.exists(save_path):
                print(f"❌ Knowledge base path does not exist: {save_path}")
                return False
                
            # Load FAISS index
            index_path = os.path.join(save_path, 'ipc_complete.index')
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
            else:
                print(f"❌ FAISS index not found: {index_path}")
                return False
            
            # Load sections data
            pkl_path = os.path.join(save_path, 'ipc_complete.pkl')
            if os.path.exists(pkl_path):
                with open(pkl_path, 'rb') as f:
                    self.sections = pickle.load(f)
            else:
                print(f"❌ Sections data not found: {pkl_path}")
                return False
            
            print(f"✅ Knowledge base loaded from {save_path}")
            print(f"📊 Loaded {len(self.sections)} sections")
            return True
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            return False

# Test function
def create_test_knowledge_base():
    """Create a test knowledge base with essential sections"""
    kb = IPCKnowledgeBase()
    
    # Create minimal test data
    test_data = {
        "sections": [
            {
                "section": "511",
                "title": "Attempts to commit offenses",
                "description": "Punishment for attempting to commit offenses punishable with imprisonment for life or other imprisonment",
                "punishment": "Imprisonment up to one-half of the maximum term or fine or both",
                "chapter": "Attempts"
            },
            {
                "section": "302",
                "title": "Punishment for murder",
                "description": "Whoever commits murder shall be punished with death or imprisonment for life",
                "punishment": "Death or imprisonment for life and fine",
                "chapter": "Offenses Affecting Life"
            },
            {
                "section": "420",
                "title": "Cheating and dishonestly inducing delivery of property",
                "description": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person",
                "punishment": "Imprisonment up to 7 years and fine",
                "chapter": "Cheating"
            }
        ]
    }
    
    # Save test data
    os.makedirs('data', exist_ok=True)
    with open('data/ipc_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2)
    
    # Load and create knowledge base
    kb.load_ipc_data('data/ipc_test_data.json')
    kb.create_embeddings()
    kb.save_knowledge_base('knowledge_base/ipc_complete')
    
    print("🎉 Test knowledge base created successfully!")

if __name__ == "__main__":
    create_test_knowledge_base()