#!/usr/bin/env python3
"""
Model Download Script for Semantic Search Chatbot

This script pre-downloads the sentence transformer model during Docker build
to avoid downloading it at runtime. This improves startup time and enables
offline usage.

The model 'all-MiniLM-L6-v2' is chosen for:
- Small size (~80MB) suitable for resource-constrained environments
- Good performance on semantic similarity tasks
- Fast inference time
"""

import os
from sentence_transformers import SentenceTransformer

def download_model():
    """
    Download and cache the sentence transformer model.
    
    The model will be saved to the default cache directory or
    to a local models/ folder if specified.
    """
    print("Downloading sentence transformer model...")
    
    # Create models directory if it doesn't exist
    models_dir = './models'
    os.makedirs(models_dir, exist_ok=True)
    
    try:
        # Download the model - this will cache it locally
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Save to local directory for offline usage
        model_path = os.path.join(models_dir, 'all-MiniLM-L6-v2')
        model.save(model_path)
        
        print(f"✓ Model downloaded and saved to {model_path}")
        print(f"Model size: ~80MB")
        
        # Test the model with a sample sentence
        test_embedding = model.encode(["This is a test sentence"])
        print(f"✓ Model test successful - embedding shape: {test_embedding.shape}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {str(e)}")
        raise

if __name__ == "__main__":
    download_model()