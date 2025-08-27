"""Factory classes for creating application components."""

from .data_loader import DataLoader
from .search_engine import SearchEngine
from .formatter import ResultFormatter
from .search_strategies import CosineSimilarityStrategy
from config import SearchConfig, DataConfig


class ComponentFactory:
    """Factory for creating application components."""
    
    @staticmethod
    def create_data_loader(config: DataConfig) -> DataLoader:
        return DataLoader(config)
    
    @staticmethod
    def create_search_engine(config: SearchConfig) -> SearchEngine:
        return SearchEngine(config, CosineSimilarityStrategy())
    
    @staticmethod
    def create_formatter() -> ResultFormatter:
        return ResultFormatter()