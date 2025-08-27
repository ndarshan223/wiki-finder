#!/bin/bash

# SDLC Tools Semantic Search Chatbot - Local Setup Script

set -e

echo "🔍 SDLC Tools Semantic Search Chatbot Setup"
echo "==========================================="

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required. Install Python 3.8+"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
echo "🔧 Setting up environment..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create data folder
if [ ! -d "data" ]; then
    mkdir -p data
fi

# Check for data files
data_files=$(find data -name "*.csv" -o -name "*.xlsx" 2>/dev/null | wc -l)
if [ "$data_files" -eq 0 ]; then
    echo "⚠️  No data files in data/ folder"
    echo "   Add Excel/CSV files with: Tool, Action, Summary, Confluence Link"
fi

echo "✅ Setup complete!"
echo "🚀 Starting application at http://localhost:8080"
echo "   Press Ctrl+C to stop"

# Run the application
python main.py