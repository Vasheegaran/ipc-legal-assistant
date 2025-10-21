import os
from dotenv import load_dotenv
import groq

def test_updated_models():
    """Test Groq API with updated models"""
    print("🧪 Testing Groq API with Updated Models...")
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ API key not found")
        return False
    
    # Available models (free tier)
    models = [
        "llama-3.1-8b-instant",      # Fastest, good for chat
        "llama-3.1-70b-versatile",   # More powerful, slower
        "mixtral-8x7b-32768",        # Good balance
    ]
    
    for model in models:
        try:
            client = groq.Client(api_key=api_key)
            
            print(f"\n🔧 Testing model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "What is 2+2? Answer in one word."}],
                max_tokens=10,
                temperature=0.1
            )
            
            print(f"✅ {model}: SUCCESS")
            print(f"   Response: {response.choices[0].message.content}")
            
        except Exception as e:
            print(f"❌ {model}: FAILED - {e}")
    
    return True

if __name__ == "__main__":
    test_updated_models()