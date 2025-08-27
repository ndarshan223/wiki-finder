from sentence_transformers import SentenceTransformer
import os

def download_model():
    """Download the model locally for offline use"""
    print("Downloading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Save model locally
    model_path = './models/all-MiniLM-L6-v2'
    os.makedirs('./models', exist_ok=True)
    model.save(model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    download_model()