"""
Setup script for Enhanced CUAD Analyzer with Groq API
"""
import os
import sys

def setup_environment():
    """Setup environment and dependencies"""
    
    print("🚀 Enhanced CUAD Analyzer Setup")
    print("=" * 50)
    
    # Check if Groq API key is set
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("\n⚠️  Groq API Key Setup Required")
        print("To get full functionality, you need a Groq API key:")
        print("1. Visit: https://console.groq.com/")
        print("2. Sign up for a free account")
        print("3. Generate an API key")
        print("4. Set environment variable: GROQ_API_KEY=your_key_here")
        print("\nFor Windows PowerShell:")
        print("$env:GROQ_API_KEY='your_key_here'")
        print("\nFor Windows Command Prompt:")
        print("set GROQ_API_KEY=your_key_here")
        print("\nNote: The analyzer will work without Groq but with limited features")
    else:
        print("✅ Groq API key found!")
    
    # Check required packages
    required_packages = [
        'torch',
        'transformers',
        'flask',
        'requests',
        'numpy'
    ]
    
    print(f"\n📦 Checking required packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ All packages are installed!")
    
    # Check CUDA availability
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🚀 CUDA available! GPU: {torch.cuda.get_device_name()}")
        else:
            print("💻 CUDA not available, using CPU (slower but functional)")
    except:
        pass
    
    return True

def run_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running Basic Tests...")
    
    try:
        from enhanced_analyzer import EnhancedCUADAnalyzer
        
        # Test CUAD model loading
        print("Loading CUAD model...")
        analyzer = EnhancedCUADAnalyzer('./')
        print("✅ CUAD model loaded successfully")
        
        # Test basic analysis
        test_contract = """
        This Software License Agreement is governed by California law.
        The payment terms require $100 monthly payments.
        Either party may terminate with 30 days notice.
        """
        
        print("Testing contract analysis...")
        result = analyzer.answer_question_advanced(test_contract, "governing_law")
        
        if result and result.get('answer'):
            print("✅ Contract analysis working")
            print(f"Sample result: {result['answer'][:50]}...")
        else:
            print("⚠️  Contract analysis may have issues")
        
        # Test Groq integration
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            print("Testing Groq API connection...")
            groq_result = analyzer.analyze_with_groq(test_contract, "comprehensive")
            if groq_result and not groq_result.get('error'):
                print("✅ Groq API working")
            else:
                print(f"⚠️  Groq API issue: {groq_result.get('error', 'Unknown error')}")
        else:
            print("⚠️  Groq API not configured (optional)")
        
        print("\n✅ Basic tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples:")
    print("=" * 30)
    
    print("\n1. Start Enhanced Web Interface:")
    print("   python enhanced_app.py")
    print("   Then visit: http://localhost:5001")
    
    print("\n2. Command Line Analysis:")
    print("""
from enhanced_analyzer import EnhancedCUADAnalyzer

analyzer = EnhancedCUADAnalyzer()
contract = "Your contract text here..."
results = analyzer.analyze_contract_comprehensive(contract)
print(results)
""")
    
    print("\n3. Risk Assessment Only:")
    print("""
risk_assessment = analyzer.assess_risks(contract_text, cuad_results)
print(f"Risk Level: {risk_assessment['overall_risk']}")
""")
    
    print("\n📱 App Agreement Features:")
    print("- Data privacy analysis")
    print("- App permissions review")
    print("- Subscription terms analysis")
    print("- User content ownership")
    print("- GDPR/CCPA compliance checks")
    
    print("\n⚠️  Risk Assessment Features:")
    print("- Automated risk scoring")
    print("- High/Medium/Low risk categorization")
    print("- Legal red flag detection")
    print("- Contract type-specific risks")
    print("- Negotiation recommendations")

def main():
    """Main setup function"""
    print("Enhanced CUAD Contract Analyzer Setup\n")
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup incomplete. Please install missing packages.")
        return
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed. The system may still work but with reduced functionality.")
    
    # Show usage examples
    show_usage_examples()
    
    print("\n🎉 Setup Complete!")
    print("\nNext Steps:")
    print("1. Set GROQ_API_KEY environment variable (optional but recommended)")
    print("2. Run: python enhanced_app.py")
    print("3. Open: http://localhost:5001")
    print("\nFor issues, check that your CUAD model files are in the current directory.")

if __name__ == "__main__":
    main()
