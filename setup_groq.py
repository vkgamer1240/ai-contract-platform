"""
Simple Groq API Setup Script
============================
"""

import os
import sys

def main():
    print("🔑 GROQ API SETUP")
    print("=" * 30)
    print("To unlock advanced features, you need a FREE Groq API key!")
    print("\n📋 Steps:")
    print("1. Go to: https://console.groq.com/")
    print("2. Sign up (free)")
    print("3. Get API key (starts with 'gsk_')")
    print("4. Enter it below")
    
    api_key = input("\n🔑 Enter your Groq API key: ").strip()
    
    if api_key and api_key.startswith('gsk_'):
        # Save to .env file
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}\n")
        
        # Set for current session
        os.environ['GROQ_API_KEY'] = api_key
        
        print("✅ API key saved successfully!")
        print("🚀 Now run: python enhanced_app.py")
        
        # Test the key
        print("\n🧪 Testing API key...")
        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
            if response.status_code == 200:
                print("✅ API key works perfectly!")
            else:
                print("⚠️  API key might have issues")
        except:
            print("⚠️  Could not test API key (network issue)")
            
    elif api_key:
        print("❌ Invalid API key format. Should start with 'gsk_'")
        print("💡 Get your key from: https://console.groq.com/")
    else:
        print("⏭️  Skipping Groq setup")
        print("💡 You can still use the basic CUAD model")

if __name__ == "__main__":
    main()
