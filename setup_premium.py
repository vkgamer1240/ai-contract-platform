"""
Comprehensive Setup Script for Premium Contract Analysis Platform
================================================================
This script helps users set up the enhanced contract analysis system with all dependencies,
API configurations, and testing capabilities.
"""
import os
import sys
import subprocess
import json
import requests
from pathlib import Path

class PremiumSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.requirements = [
            "torch>=1.9.0",
            "transformers>=4.20.0",
            "flask>=2.0.0",
            "requests>=2.25.0",
            "pandas>=1.3.0",
            "numpy>=1.21.0"
        ]
        
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Premium Contract Analysis Platform Setup")
        print("=" * 50)
        
        # Step 1: Check Python version
        self.check_python_version()
        
        # Step 2: Install dependencies
        self.install_dependencies()
        
        # Step 3: Verify model files
        self.verify_model_files()
        
        # Step 4: Setup Groq API
        self.setup_groq_api()
        
        # Step 5: Test the system
        self.test_system()
        
        # Step 6: Create sample environment file
        self.create_env_file()
        
        print("\n✅ Setup completed successfully!")
        self.print_usage_instructions()
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("\n1. Checking Python version...")
        
        python_version = sys.version_info
        if python_version.major != 3 or python_version.minor < 8:
            print("❌ Python 3.8 or higher is required")
            print(f"   Current version: {python_version.major}.{python_version.minor}")
            sys.exit(1)
        
        print(f"✅ Python {python_version.major}.{python_version.minor} is compatible")
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n2. Installing dependencies...")
        
        try:
            # Check if pip is available
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            
            # Install requirements
            for package in self.requirements:
                print(f"   Installing {package}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"⚠️  Warning: Failed to install {package}")
                    print(f"   Error: {result.stderr}")
                else:
                    print(f"✅ {package} installed")
            
        except subprocess.CalledProcessError:
            print("❌ pip is not available. Please install pip first.")
            sys.exit(1)
    
    def verify_model_files(self):
        """Verify that CUAD model files are present"""
        print("\n3. Verifying model files...")
        
        required_files = [
            "config.json",
            "pytorch_model.bin",
            "tokenizer_config.json",
            "vocab.json",
            "merges.txt"
        ]
        
        missing_files = []
        for file in required_files:
            file_path = self.base_dir / file
            if not file_path.exists():
                missing_files.append(file)
            else:
                print(f"✅ {file} found")
        
        if missing_files:
            print(f"\n❌ Missing model files: {', '.join(missing_files)}")
            print("   Please ensure you have the complete CUAD model files.")
            print("   You can download them from: https://huggingface.co/microsoft/roberta-base-squad2")
            return False
        
        print("✅ All model files are present")
        return True
    
    def setup_groq_api(self):
        """Setup Groq API configuration"""
        print("\n4. Setting up Groq API...")
        
        # Check if API key is already set
        existing_key = os.getenv('GROQ_API_KEY')
        if existing_key:
            print(f"✅ Groq API key already set: {existing_key[:8]}...")
            if self.test_groq_api(existing_key):
                return
        
        print("   Groq API enhances the analysis with advanced AI capabilities.")
        print("   You can get a free API key from: https://console.groq.com/")
        
        while True:
            api_key = input("\n   Enter your Groq API key (or press Enter to skip): ").strip()
            
            if not api_key:
                print("⚠️  Skipping Groq API setup. Some features will be limited.")
                break
            
            if self.test_groq_api(api_key):
                # Save to environment file
                env_file = self.base_dir / ".env"
                with open(env_file, "w") as f:
                    f.write(f"GROQ_API_KEY={api_key}\n")
                print(f"✅ Groq API key saved to {env_file}")
                
                # Set for current session
                os.environ['GROQ_API_KEY'] = api_key
                break
            else:
                print("❌ Invalid API key. Please try again.")
    
    def test_groq_api(self, api_key):
        """Test if Groq API key is valid"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Groq API key is valid")
                return True
            else:
                print(f"❌ Groq API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Groq API test error: {str(e)}")
            return False
    
    def test_system(self):
        """Test the contract analysis system"""
        print("\n5. Testing system...")
        
        try:
            # Test CUAD model loading
            print("   Testing CUAD model...")
            from enhanced_analyzer import EnhancedCUADAnalyzer
            
            analyzer = EnhancedCUADAnalyzer('./')
            print("✅ CUAD model loaded successfully")
            
            # Test with sample text
            sample_text = """
            This Software License Agreement is entered into between Company ABC and the User.
            The agreement is governed by the laws of California.
            Either party may terminate this agreement with 30 days written notice.
            The maximum liability under this agreement is limited to $1,000.
            """
            
            result = analyzer.answer_question_advanced(sample_text, "governing_law")
            if result and result.get('answer'):
                print("✅ CUAD analysis test successful")
            else:
                print("⚠️  CUAD analysis test returned no results")
            
            # Test advanced features
            print("   Testing advanced features...")
            from advanced_features import AdvancedContractProcessor
            
            processor = AdvancedContractProcessor(analyzer)
            contract_type = analyzer.detect_contract_type(sample_text)
            print(f"✅ Contract type detection: {contract_type}")
            
            # Test Groq if available
            if os.getenv('GROQ_API_KEY'):
                print("   Testing Groq integration...")
                groq_result = analyzer.analyze_with_groq(sample_text, "comprehensive")
                if 'error' not in groq_result:
                    print("✅ Groq integration test successful")
                else:
                    print(f"⚠️  Groq integration test failed: {groq_result['error']}")
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("   Some dependencies may not be installed correctly.")
        except Exception as e:
            print(f"❌ System test failed: {e}")
    
    def create_env_file(self):
        """Create environment configuration file"""
        print("\n6. Creating configuration files...")
        
        # Create .env file if it doesn't exist
        env_file = self.base_dir / ".env"
        if not env_file.exists():
            with open(env_file, "w") as f:
                f.write("# Premium Contract Analysis Platform Configuration\n")
                f.write("# Set your Groq API key here for enhanced features\n")
                f.write("GROQ_API_KEY=your_groq_api_key_here\n")
                f.write("\n# Flask configuration\n")
                f.write("FLASK_ENV=development\n")
                f.write("FLASK_DEBUG=True\n")
            
            print(f"✅ Configuration file created: {env_file}")
        
        # Create startup script
        startup_script = self.base_dir / "start_premium.py"
        with open(startup_script, "w") as f:
            f.write('''#!/usr/bin/env python3
"""
Premium Contract Analysis Platform Startup Script
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Start the premium app
if __name__ == "__main__":
    from premium_app import app, load_enhanced_system
    
    print("Loading Premium Contract Analysis Platform...")
    load_enhanced_system()
    
    print("Starting web interface...")
    print("Access at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
''')
        
        print(f"✅ Startup script created: {startup_script}")
    
    def print_usage_instructions(self):
        """Print usage instructions"""
        print("\n" + "=" * 50)
        print("🎉 PREMIUM CONTRACT ANALYSIS PLATFORM READY!")
        print("=" * 50)
        
        print("\n📚 How to use:")
        print("1. Run the web interface:")
        print("   python premium_app.py")
        print("   OR")
        print("   python start_premium.py")
        
        print("\n2. Access the web interface:")
        print("   Open your browser and go to: http://localhost:5000")
        
        print("\n3. Available features:")
        print("   📄 Single Contract Analysis - Comprehensive analysis of individual contracts")
        print("   📚 Batch Processing - Analyze multiple contracts simultaneously")
        print("   ⚖️  Contract Comparison - Side-by-side comparison of two contracts")
        print("   ✅ Compliance Check - App store compliance verification")
        print("   🚨 Risk Assessment - Detailed risk analysis with scoring")
        
        print("\n4. API Usage (for developers):")
        print("   All features are available via REST API endpoints")
        print("   Check premium_app.py for endpoint documentation")
        
        print("\n5. Sample contracts:")
        print("   Use the built-in sample contracts to test the system")
        print("   Includes mobile app ToS, privacy policies, and SaaS agreements")
        
        if not os.getenv('GROQ_API_KEY'):
            print("\n⚠️  Note: Groq API not configured")
            print("   Some advanced AI features will be limited")
            print("   Get your free API key from: https://console.groq.com/")
        
        print("\n📖 For more information:")
        print("   Check the README.md file")
        print("   Review the testing_guide.py for optimal usage")
        
        print("\n💡 Tips:")
        print("   - Use sample contracts to get familiar with the interface")
        print("   - Try different analysis types to see comprehensive results")
        print("   - Export reports for detailed documentation")
        print("   - Use batch processing for comparing multiple contracts")

def main():
    """Main setup function"""
    try:
        setup = PremiumSetup()
        setup.run_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
