"""Configuration settings for the application."""

from dataclasses import dataclass
from typing import List


@dataclass
class SearchConfig:
    """Search engine configuration."""
    model_name: str = 'all-MiniLM-L6-v2'
    model_path: str = './models'
    similarity_threshold: float = 0.1
    max_results: int = 5


@dataclass
class DataConfig:
    """Data loading configuration."""
    data_folder: str = "data"
    required_columns: List[str] = None
    
    def __post_init__(self):
        if self.required_columns is None:
            self.required_columns = ['Tool', 'Action', 'Summary', 'Confluence Link']


@dataclass
class UIConfig:
    """UI configuration."""
    title: str = "SDLC Tools Semantic Search"
    server_name: str = "0.0.0.0"
    server_port: int = 8080
    chat_height: int = 500


@dataclass
class AppConfig:
    """Main application configuration."""
    search: SearchConfig = None
    data: DataConfig = None
    ui: UIConfig = None
    
    def __post_init__(self):
        if self.search is None:
            self.search = SearchConfig()
        if self.data is None:
            self.data = DataConfig()
        if self.ui is None:
            self.ui = UIConfig()