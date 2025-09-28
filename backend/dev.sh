#!/bin/bash

# VueLites Backend Development Server
# Simple script to start the development server

echo "🚀 VueLites Backend Development"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run: python3 -m venv venv && source venv/bin/activate && pip install -r ../requirements.txt"
    exit 1
fi

# Activate virtual environment and start server
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🌐 Starting development server..."
echo "   Backend: http://localhost:5001"
echo "   Frontend: http://localhost:3000 (start separately)"
echo "================================"

python dev_server.py