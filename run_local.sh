#!/bin/bash

# SDLC Tools Semantic Search Chatbot - Local Setup Script
# This script handles environment setup and launches the application

set -e  # Exit on any error

echo "🚀 Starting SDLC Tools Semantic Search Chatbot..."
echo "================================================"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Setup virtual environment
echo "🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Check if data files exist, copy sample data if needed
if [ ! -f "data/sdlc_tools_data.csv" ]; then
    echo "📁 Setting up sample data..."
    
    # Create data directory if it doesn't exist
    mkdir -p data
    
    # Copy sample data if available
    if [ -f "sdlc_tools_data.csv" ]; then
        cp sdlc_tools_data.csv data/ 2>/dev/null && echo "✅ Sample data copied to data/ folder" || echo "⚠️  Could not copy sample data"
    else
        echo "⚠️  No sample data found. Please add Excel/CSV files to data/ folder"
    fi
else
    echo "✅ Data files found in data/ folder"
fi

# Check and install Python dependencies
echo "📦 Checking Python dependencies..."
if ! python -c "import gradio, pandas, sentence_transformers" 2>/dev/null; then
    echo "📥 Installing required dependencies..."
    echo "This may take a few minutes on first run..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    echo "✅ Dependencies installed successfully"
else
    echo "✅ All dependencies are already installed"
fi

# Check available memory (Linux/macOS)
if command_exists free; then
    available_mem=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
    echo "💾 Available memory: ${available_mem}GB"
    
    if (( $(echo "$available_mem < 2" | bc -l) )); then
        echo "⚠️  Warning: Low memory detected. Application may run slowly."
    fi
fi

# Launch the application
echo "🌐 Launching application..."
echo "📍 Access the chatbot at: http://localhost:8080"
echo "🛑 Press Ctrl+C to stop the application"
echo "================================================"

# Run the Python application
python app.py