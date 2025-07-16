#!/usr/bin/env python3
"""
Full Stack Startup Script
=========================
Coordinates the React frontend and Flask backend for the contract analysis platform.
"""
import subprocess
import sys
import os
import time
import signal
import requests
from pathlib import Path
import threading

class FullStackManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_dir = self.base_dir / "project"
        self.flask_process = None
        self.react_process = None
        
    def start_flask_server(self):
        """Start the Flask backend"""
        print("🚀 Starting Flask Contract Analysis Server...")
        
        # Change to base directory for Flask app
        os.chdir(self.base_dir)
        
        try:
            self.flask_process = subprocess.Popen([
                sys.executable, "premium_app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for Flask server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get("http://localhost:5000/api/health_check", timeout=2)
                    if response.status_code == 200:
                        print("✅ Flask server started at http://localhost:5000")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"⏳ Waiting for Flask server... ({attempt + 1}/{max_attempts})")
            
            print("❌ Flask server failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Flask server: {e}")
            return False
    
    def start_react_server(self):
        """Start the React frontend"""
        print("🚀 Starting React Frontend Server...")
        
        # Change to project directory for React app
        os.chdir(self.project_dir)
        
        try:
            # Check if node_modules exists
            if not (self.project_dir / "node_modules").exists():
                print("📦 Installing npm dependencies...")
                npm_install = subprocess.run(["npm", "install"], capture_output=True, text=True)
                if npm_install.returncode != 0:
                    print(f"❌ npm install failed: {npm_install.stderr}")
                    return False
            
            # Start React dev server
            self.react_process = subprocess.Popen([
                "npm", "run", "dev"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for React server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get("http://localhost:5173", timeout=2)
                    if response.status_code == 200:
                        print("✅ React server started at http://localhost:5173")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"⏳ Waiting for React server... ({attempt + 1}/{max_attempts})")
            
            print("✅ React server should be starting (may take a moment to fully load)")
            return True
            
        except Exception as e:
            print(f"❌ Error starting React server: {e}")
            return False
    
    def start_full_stack(self):
        """Start both Flask and React servers"""
        print("🚀 Starting Full Stack Contract Analysis Platform")
        print("=" * 60)
        
        # Start Flask server first
        flask_success = self.start_flask_server()
        if not flask_success:
            print("❌ Failed to start Flask server. Aborting.")
            return False
        
        # Wait a moment
        time.sleep(2)
        
        # Start React server
        react_success = self.start_react_server()
        if not react_success:
            print("❌ Failed to start React server.")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 FULL STACK PLATFORM READY!")
        print("=" * 60)
        print("📱 Frontend (Landing Page): http://localhost:5173")
        print("🔧 Backend (Contract Analysis): http://localhost:5000")
        print("\n🎯 User Flow:")
        print("1. Open http://localhost:5173 in your browser")
        print("2. Click 'Get Started' button")
        print("3. Login/Register (use any email/password)")
        print("4. Choose 'Contract Analysis' from the service selection")
        print("5. Launch the Premium Contract Analysis Platform")
        print("\n⚠️  Press Ctrl+C to stop both servers")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            self.stop_servers()
    
    def stop_servers(self):
        """Stop both servers"""
        if self.flask_process:
            print("🛑 Stopping Flask server...")
            self.flask_process.terminate()
            self.flask_process.wait()
        
        if self.react_process:
            print("🛑 Stopping React server...")
            self.react_process.terminate()
            self.react_process.wait()
        
        print("✅ All servers stopped")
    
    def check_status(self):
        """Check status of both servers"""
        print("🔍 Checking Server Status")
        print("=" * 30)
        
        # Check Flask
        try:
            response = requests.get("http://localhost:5000/api/health_check", timeout=2)
            if response.status_code == 200:
                data = response.json()
                groq_status = "✅ Available" if data.get("groq_available") else "❌ Not configured"
                print(f"Flask Backend: ✅ Running (Groq: {groq_status})")
            else:
                print("Flask Backend: ❌ Error")
        except:
            print("Flask Backend: ❌ Not running")
        
        # Check React
        try:
            response = requests.get("http://localhost:5173", timeout=2)
            if response.status_code == 200:
                print("React Frontend: ✅ Running")
            else:
                print("React Frontend: ❌ Error")
        except:
            print("React Frontend: ❌ Not running")

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Full Stack Contract Analysis Platform")
    parser.add_argument("action", choices=["start", "status", "flask-only", "react-only"], 
                       help="Action to perform", nargs="?", default="start")
    
    args = parser.parse_args()
    manager = FullStackManager()
    
    if args.action == "start":
        manager.start_full_stack()
    elif args.action == "status":
        manager.check_status()
    elif args.action == "flask-only":
        manager.start_flask_server()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_servers()
    elif args.action == "react-only":
        manager.start_react_server()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_servers()

if __name__ == "__main__":
    main()
