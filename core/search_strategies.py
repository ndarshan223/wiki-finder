"""Search strategy implementations for extensibility."""

from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import pandas as pd


class SearchStrategy(ABC):
    """Abstract base class for search strategies."""
    
    @abstractmethod
    def search(self, query_embedding: np.ndarray, data_embeddings: np.ndarray, 
               data: pd.DataFrame, top_k: int, threshold: float) -> List[Dict[str, Any]]:
        """Perform search using this strategy."""
        pass


class CosineSimilarityStrategy(SearchStrategy):
    """Standard cosine similarity search strategy."""
    
    def search(self, query_embedding: np.ndarray, data_embeddings: np.ndarray, 
               data: pd.DataFrame, top_k: int, threshold: float) -> List[Dict[str, Any]]:
        """Search using cosine similarity."""
        similarities = cosine_similarity(query_embedding, data_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > threshold:
                result = {
                    'tool': data.iloc[idx]['Tool'],
                    'action': data.iloc[idx]['Action'],
                    'summary': data.iloc[idx]['Summary'],
                    'link': data.iloc[idx]['Confluence Link'],
                    'similarity': similarities[idx]
                }
                results.append(result)
        
        return results


