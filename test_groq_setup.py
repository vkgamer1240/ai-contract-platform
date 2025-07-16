"""
Test Groq API Key Configuration
===============================
This script tests if your Groq API key is working correctly.
"""
import os
import requests
import json
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"✅ Found .env file: {env_file}")
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                    print(f"✅ Set {key}")
    else:
        print("❌ .env file not found")

def test_groq_api():
    """Test the Groq API with your key"""
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    print(f"✅ Found API key: {api_key[:8]}...")
    
    # Test API call
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful contract analysis assistant."
                },
                {
                    "role": "user",
                    "content": "Analyze this simple contract clause: 'This agreement is governed by California law.' What does this mean?"
                }
            ],
            "temperature": 0.1,
            "max_tokens": 200
        }
        
        print("🔄 Testing Groq API...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            print("✅ Groq API test successful!")
            print(f"📝 Sample analysis: {analysis[:200]}...")
            return True
        else:
            print(f"❌ Groq API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Groq API test failed: {str(e)}")
        return False

def test_enhanced_analyzer():
    """Test the enhanced analyzer with Groq API"""
    try:
        print("\n🔄 Testing Enhanced CUAD Analyzer...")
        from enhanced_analyzer import EnhancedCUADAnalyzer
        
        # Initialize with the API key
        analyzer = EnhancedCUADAnalyzer('./', groq_api_key=os.getenv('GROQ_API_KEY'))
        
        # Test with a simple contract
        sample_contract = """
        SOFTWARE LICENSE AGREEMENT
        
        This Software License Agreement is governed by the laws of Delaware.
        Either party may terminate this agreement with 30 days written notice.
        The maximum liability under this agreement is limited to $1,000.
        User data will be collected and may be shared with third parties.
        """
        
        print("🔄 Testing contract analysis...")
        
        # Test CUAD analysis
        governing_law = analyzer.answer_question_advanced(sample_contract, "governing_law")
        print(f"✅ CUAD Analysis - Governing Law: {governing_law['answer']}")
        
        # Test Groq analysis
        groq_result = analyzer.analyze_with_groq(sample_contract, "comprehensive")
        if 'error' not in groq_result:
            print("✅ Groq Analysis successful!")
            print(f"📝 Groq insight: {groq_result['analysis'][:150]}...")
        else:
            print(f"❌ Groq Analysis failed: {groq_result['error']}")
        
        # Test comprehensive analysis
        comprehensive = analyzer.analyze_contract_comprehensive(sample_contract)
        print(f"✅ Comprehensive Analysis - Contract Type: {comprehensive['contract_type']}")
        print(f"✅ Risk Score: {comprehensive['risk_assessment']['risk_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced analyzer test failed: {str(e)}")
        return False

def main():
    print("🚀 GROQ API CONFIGURATION TEST")
    print("=" * 50)
    
    # Load environment file
    load_env_file()
    
    # Test Groq API
    if test_groq_api():
        print("\n✅ Groq API is working correctly!")
        
        # Test enhanced analyzer
        if test_enhanced_analyzer():
            print("\n🎉 SETUP COMPLETE!")
            print("=" * 50)
            print("Your enhanced contract analysis system is ready!")
            print("\n📚 Next steps:")
            print("1. Run the web interface: python premium_app.py")
            print("2. Or run enhanced app: python enhanced_app.py")
            print("3. Or test individual contracts: python advanced_test.py")
            print("\n🌐 Web interface will be at: http://localhost:5000")
        else:
            print("\n⚠️ Enhanced analyzer had issues, but Groq API works")
    else:
        print("\n❌ Groq API test failed. Please check your API key.")

if __name__ == "__main__":
    main()
