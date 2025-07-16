#!/usr/bin/env python3
"""
Quick test of Groq API functionality
"""
import os
from groq_enhancement import GroqEnhancement

def test_groq_api():
    print("🧪 Testing Groq API Integration...")
    
    # Check if API key is loaded
    api_key = os.getenv('GROQ_API_KEY')
    print(f"🔑 API Key present: {bool(api_key)}")
    if api_key:
        print(f"🔑 API Key starts with: {api_key[:10]}...")
    
    # Initialize Groq enhancer
    groq = GroqEnhancement()
    print(f"⚡ Groq available: {groq.is_available()}")
    
    if groq.is_available():
        print("🚀 Testing simple summary...")
        test_contract = """
        This application privacy policy describes how we collect and use your personal information when you use our mobile app. We may collect device information, location data, and usage analytics. You may request data deletion, but some information may remain in backups. We do not knowingly collect data from children under 13, but age verification is limited.
        """
        
        # Test simple summary
        result = groq.enhance_analysis(test_contract, "simple_summary")
        if result:
            print("✅ Simple summary successful!")
            print(f"📄 Summary: {result['analysis'][:200]}...")
        else:
            print("❌ Simple summary failed")
            
        # Test risk highlighting
        print("🎨 Testing risk highlighting...")
        risk_result = groq.enhance_analysis(test_contract, "risk_highlighting")
        if risk_result:
            print("✅ Risk highlighting successful!")
            print(f"🎯 Risk analysis: {risk_result['analysis'][:200]}...")
        else:
            print("❌ Risk highlighting failed")
    else:
        print("❌ Groq API not available")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    test_groq_api()
