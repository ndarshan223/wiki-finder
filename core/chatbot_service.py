"""Main chatbot service orchestrating all components."""

from .data_loader import DataLoader
from .search_engine import SearchEngine
from .formatter import ResultFormatter
from config import AppConfig
from typing import Dict, Any, Optional


class ChatbotService:
    """Main service class that orchestrates all chatbot functionality."""
    
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()
        self.data_loader = DataLoader(self.config.data)
        self.search_engine = SearchEngine(self.config.search)
        self.formatter = ResultFormatter()
        self._initialize()
    
    def _initialize(self):
        """Initialize the chatbot by loading data and creating embeddings."""
        print("Initializing Semantic Search Chatbot...")
        
        # Load data
        data = self.data_loader.load_files()
        if data is not None:
            self.search_engine.index_data(data)
        else:
            print("ERROR: No valid data files could be loaded")
    
    def search(self, query: str, top_k: Optional[int] = None) -> str:
        """Perform search and return formatted results."""
        if not query or not query.strip():
            return "Please enter a search query."
        
        # Check if system is ready
        status = self.search_engine.get_status()
        if not status['data_indexed']:
            return "❌ No data loaded from data/ folder. Please check data files and restart the application."
        
        # Use config default if not specified
        if top_k is None:
            top_k = self.config.search.max_results
        
        # Perform search
        results = self.search_engine.search(query.strip(), top_k, self.config.search.similarity_threshold)
        return self.formatter.format_search_results(results, query)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return self.search_engine.get_status()
    
    def get_record_count(self) -> int:
        """Get number of loaded records."""
        status = self.get_status()
        return status.get('record_count', 0)
    
    def reload_data(self):
        """Reload data from files."""
        self._initialize()