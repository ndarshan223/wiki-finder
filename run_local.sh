#!/bin/bash

echo "Setting up Semantic Search Chatbot..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download model
echo "Downloading AI model (one-time setup)..."
python download_model.py

# Create sample data
echo "Creating sample data..."
python sample_data.py

# Run the application
echo "Starting the chatbot application..."
echo "Access the application at: http://localhost:7860"
python app.py