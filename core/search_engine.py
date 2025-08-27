"""Semantic search engine module."""

from sentence_transformers import SentenceTransformer
import pandas as pd
import os
from typing import List, Dict, Any, Optional
from config import SearchConfig
from .search_strategies import SearchStrategy, CosineSimilarityStrategy


class SearchEngine:
    """Handles semantic search operations."""
    
    def __init__(self, config: SearchConfig, search_strategy: Optional[SearchStrategy] = None):
        self.config = config
        self.model_name = config.model_name
        self.model_path = config.model_path
        self.model = None
        self.embeddings = None
        self.data = None
        self.search_strategy = search_strategy or CosineSimilarityStrategy()
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        local_model_path = f'{self.model_path}/{self.model_name}'
        
        if os.path.exists(local_model_path):
            print(f"Loading local model from {local_model_path}")
            self.model = SentenceTransformer(local_model_path)
        else:
            print("Downloading sentence transformer model...")
            self.model = SentenceTransformer(self.model_name)
    
    def index_data(self, data: pd.DataFrame):
        """Create embeddings for the provided data."""
        if data is None or data.empty:
            print("ERROR: No data to index")
            return
        
        self.data = data
        print("Generating embeddings for semantic search...")
        
        self.embeddings = self.model.encode(
            data['searchable_text'].tolist(),
            show_progress_bar=True
        )
        
        print(f"✓ Successfully indexed {len(data)} records")
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.1) -> List[Dict[str, Any]]:
        """Perform semantic search."""
        if self.data is None or self.embeddings is None:
            return []
        
        if not query or not query.strip():
            return []
        
        try:
            query_embedding = self.model.encode([query.strip()])
            return self.search_strategy.search(
                query_embedding, self.embeddings, self.data, top_k, threshold
            )
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the search engine."""
        return {
            'model_loaded': self.model is not None,
            'data_indexed': self.data is not None,
            'record_count': len(self.data) if self.data is not None else 0,
            'embeddings_ready': self.embeddings is not None
        }