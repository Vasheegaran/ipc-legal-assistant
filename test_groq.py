import os
from pathlib import Path
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment Setup...")
    
    # Check if .env file exists
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found in project root")
        return False
    
    print("✅ .env file found")
    
    # Load environment variables
    load_dotenv()
    
    # Check Groq API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    if api_key == "your_groq_api_key_here" or len(api_key) < 10:
        print("❌ GROQ_API_KEY appears to be placeholder or invalid")
        return False
    
    print(f"✅ GROQ_API_KEY found (length: {len(api_key)})")
    print(f"   Key starts with: {api_key[:10]}...")
    return True

def test_groq_api():
    """Test Groq API connectivity"""
    print("\n🧪 Testing Groq API Connectivity...")
    
    if not test_environment():
        return False
    
    try:
        import groq
        
        api_key = os.getenv("GROQ_API_KEY")
        client = groq.Client(api_key=api_key)
        
        # Simple test query
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "Just say 'API test successful!'"}],
            max_tokens=10,
            temperature=0.1
        )
        
        print("✅ Groq API test successful!")
        print(f"🤖 Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_api()
    if success:
        print("\n🎉 Groq API is ready! We can proceed to Phase 3!")
    else:
        print("\n💡 Please check your .env file and API key")