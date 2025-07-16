#!/usr/bin/env python3
"""
Server Integration Script for Contract Analysis Platform
========================================================
This script manages the startup and integration of the premium contract analysis server
with the React frontend.
"""
import subprocess
import sys
import os
import time
import signal
import requests
from pathlib import Path

class ContractAnalysisServer:
    def __init__(self):
        self.server_process = None
        self.base_dir = Path(__file__).parent
        self.server_url = "http://localhost:5000"
        
    def is_server_running(self):
        """Check if the server is already running"""
        try:
            response = requests.get(f"{self.server_url}/api/health_check", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_server(self):
        """Start the premium contract analysis server"""
        if self.is_server_running():
            print("✅ Contract Analysis Server is already running")
            return True
        
        print("🚀 Starting Premium Contract Analysis Server...")
        
        # Change to the correct directory
        os.chdir(self.base_dir)
        
        try:
            # Start the premium app
            self.server_process = subprocess.Popen([
                sys.executable, "premium_app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                if self.is_server_running():
                    print(f"✅ Server started successfully at {self.server_url}")
                    return True
                time.sleep(1)
                print(f"⏳ Waiting for server... ({attempt + 1}/{max_attempts})")
            
            print("❌ Server failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_server(self):
        """Stop the contract analysis server"""
        if self.server_process:
            print("🛑 Stopping Contract Analysis Server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("✅ Server stopped")
    
    def get_server_status(self):
        """Get detailed server status"""
        if self.is_server_running():
            try:
                response = requests.get(f"{self.server_url}/api/health_check")
                data = response.json()
                return {
                    "status": "running",
                    "url": self.server_url,
                    "groq_available": data.get("groq_available", False),
                    "timestamp": data.get("timestamp", "")
                }
            except:
                return {"status": "running", "url": self.server_url}
        else:
            return {"status": "stopped"}

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Contract Analysis Server Manager")
    parser.add_argument("action", choices=["start", "stop", "status", "restart"], 
                       help="Action to perform")
    
    args = parser.parse_args()
    server = ContractAnalysisServer()
    
    if args.action == "start":
        server.start_server()
    elif args.action == "stop":
        server.stop_server()
    elif args.action == "status":
        status = server.get_server_status()
        print(f"Server Status: {status}")
    elif args.action == "restart":
        server.stop_server()
        time.sleep(2)
        server.start_server()

if __name__ == "__main__":
    main()
