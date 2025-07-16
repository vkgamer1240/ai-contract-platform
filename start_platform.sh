#!/bin/bash
# Comprehensive startup script for the integrated platform

echo "🚀 Starting AI Contract Analysis Platform"
echo "========================================"

# Function to check if a port is in use
check_port() {
    local port=$1
    if netstat -an | grep -q ":$port.*LISTEN"; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Start Flask app (Contract Analysis)
start_flask() {
    echo "📄 Starting Contract Analysis Server (Flask)..."
    cd "c:/Users/srid1/Documents/LLMFINAL/roberta-base"
    
    if check_port 5000; then
        echo "✅ Flask server already running on port 5000"
    else
        echo "🔄 Starting Flask server..."
        start /B python premium_app.py
        echo "⏳ Waiting for Flask server to start..."
        sleep 5
    fi
}

# Start React app (Landing Page)
start_react() {
    echo "🌐 Starting Landing Page (React)..."
    cd "c:/Users/srid1/Documents/LLMFINAL/roberta-base/project"
    
    if check_port 3000; then
        echo "✅ React server already running on port 3000"
    else
        echo "🔄 Starting React development server..."
        start /B npm run dev
        echo "⏳ Waiting for React server to start..."
        sleep 10
    fi
}

# Main execution
main() {
    echo "🔍 Checking system requirements..."
    
    # Check if Python is available
    if ! command -v python &> /dev/null; then
        echo "❌ Python not found. Please install Python."
        exit 1
    fi
    
    # Check if Node.js is available
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found. Please install Node.js."
        exit 1
    fi
    
    echo "✅ System requirements met"
    echo ""
    
    # Start both servers
    start_flask
    echo ""
    start_react
    echo ""
    
    echo "🎉 Platform startup complete!"
    echo ""
    echo "📋 Access URLs:"
    echo "   Landing Page: http://localhost:3000"
    echo "   Contract Analysis: http://localhost:5000"
    echo ""
    echo "🔗 Workflow:"
    echo "1. Open http://localhost:3000 (Landing Page)"
    echo "2. Click 'Get Started'"
    echo "3. Login or Sign up"
    echo "4. Select 'Contract Analysis'"
    echo "5. System will launch the premium contract analysis app"
    echo ""
    echo "Press Ctrl+C to stop all servers"
    
    # Keep script running
    while true; do
        sleep 60
        echo "⏰ Platform running... ($(date))"
    done
}

# Execute main function
main
