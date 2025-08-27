# 🔍 SDLC Tools Semantic Search Chatbot

A semantic search-powered chatbot for SDLC (Software Development Life Cycle) tools documentation. Built with Gradio for the UI and sentence transformers for intelligent search capabilities.

## 🎯 Purpose

This application serves teams using SDLC tools by providing intelligent search across documentation for:
- **GitLab** - CI/CD, repository management, merge requests
- **Jira** - Project management, workflows, agile boards  
- **SonarQube** - Code quality, security analysis
- **Nexus** - Artifact repository management
- **CloudBees** - Jenkins pipelines, build automation
- **Confluence** - Documentation and knowledge management
- **Bitbucket** - Git repository hosting, pull requests
- **Q Whisperer** - AI-powered development assistance

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │  Semantic Search │    │   Data Layer    │
│                 │    │                  │    │                 │
│ • Chat Interface│◄──►│ • Sentence       │◄──►│ • Excel/CSV     │
│ • Query Input   │    │   Transformers   │    │   Files         │
│ • Results       │    │ • Cosine         │    │ • In-memory     │
│   Display       │    │   Similarity     │    │   Vector DB     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Local Python Setup
```bash
# Clone and navigate to project
cd chatbot

# Run setup script (handles dependencies and data)
./run_local.sh

# Or manual setup:
pip install -r requirements.txt
python main.py
```

### Option 2: Docker Setup
```bash
# Build and run with resource constraints
docker-compose up --build

# Access at http://localhost:8080 (local) or http://localhost:8080 (docker)
```

### 🌐 Application Access
- **Local Python**: http://localhost:8080
- **Docker**: http://localhost:8080
- **Interface Tabs**:
  - **Chat**: Main semantic search interface
  - **Data Management**: Upload Excel/CSV files

## 📊 Data Format

Place Excel (.xlsx) or CSV files in the `data/` folder with these columns:

| Column | Description | Example |
|--------|-------------|---------||
| **Tool** | SDLC tool name | GitLab, Jira, SonarQube |
| **Action** | Specific task/action | Setup CI/CD Pipeline |
| **Summary** | Detailed description | Configure GitLab CI/CD pipeline for automated builds and deployments |
| **Confluence Link** | Documentation URL | https://confluence.company.com/gitlab/cicd-setup |

## 🔧 Configuration

### Resource Requirements
- **Memory**: <3GB RAM (optimized for laptops)
- **CPU**: Minimal (lightweight model)
- **Storage**: ~500MB for dependencies
- **Model**: all-MiniLM-L6-v2 (~80MB)

### Environment Variables
```bash
PYTHONUNBUFFERED=1          # Better logging
PYTHONDONTWRITEBYTECODE=1   # No .pyc files
```

## 🧠 How It Works

1. **Data Loading**: Automatically scans `data/` folder for Excel/CSV files
2. **Text Processing**: Combines Tool + Action + Summary into searchable text
3. **Embedding Generation**: Converts text to 384-dimensional vectors using sentence transformers
4. **Semantic Search**: Uses cosine similarity to find relevant matches
5. **Result Ranking**: Returns top 5 results with similarity scores

### Search Algorithm
```python
# 1. Encode user query
query_embedding = model.encode([user_query])

# 2. Calculate similarities with all data
similarities = cosine_similarity(query_embedding, data_embeddings)

# 3. Rank and filter results (>10% similarity)
top_results = sorted_results[similarities > 0.1][:5]
```

## 📁 Project Structure

```
chatbot/
├── core/                  # Business logic
│   ├── chatbot_service.py # Main service orchestrator
│   ├── data_loader.py     # Data loading and preprocessing
│   ├── search_engine.py   # Semantic search operations
│   ├── formatter.py       # Result formatting
│   ├── search_strategies.py # Search algorithms
│   └── factory.py         # Component factories
├── ui/                    # User interface
│   ├── interface.py       # Gradio UI components
│   └── styles.py          # CSS styling
├── data/                  # Data files directory
├── config.py              # Configuration management
├── main.py               # Application entry point
├── app.py                # Legacy entry point
├── requirements.txt       # Python dependencies
├── run_local.sh          # Local setup script
└── docker-compose.yml    # Container setup
```

## 🔍 Usage Examples

**Query**: "How to configure GitLab CI/CD?"
**Results**: 
- GitLab - Setup CI/CD Pipeline (95% match)
- GitLab - Configure Runners (87% match)

**Query**: "Jira workflow setup"
**Results**:
- Jira - Workflow Configuration (92% match)
- Jira - Agile Boards (78% match)

## 🛠️ Development

### Data Setup
1. **Prepare Data Files**:
   ```bash
   # Move sample data to data folder (if needed)
   sudo mv sdlc_tools_data.csv data/
   # OR create your own Excel file with required columns
   ```

2. **Data Management Options**:
   - Place files directly in `data/` folder
   - Use "Data Management" tab in UI to upload files
   - Supports both Excel (.xlsx) and CSV formats

### Adding New Data
1. Place Excel/CSV files in `data/` folder
2. Ensure proper column format (Tool, Action, Summary, Confluence Link)
3. Restart application to reload data

### Customizing Search
- **Similarity threshold**: Modify `similarity_threshold` in `config.py`
- **Result count**: Change `max_results` in `config.py`
- **Model**: Replace `model_name` in `config.py`

### Performance Tuning
- **Memory**: Adjust Docker memory limits in `docker-compose.yml`
- **Batch size**: Modify embedding generation for large datasets
- **Caching**: Models are cached locally after first download

## 🐛 Troubleshooting

### Common Issues

**No data loaded**
```bash
# Check data folder and file permissions
ls -la data/
# Ensure CSV/Excel files have correct columns: Tool, Action, Summary, Confluence Link
# Verify file format and encoding
```

**Port conflicts**
```bash
# If port 8080 is in use, modify in main.py:
# demo.launch(server_port=8080)
```

**Memory errors**
```bash
# Reduce Docker memory limits or use smaller model
# Check available system memory
free -h
# For Docker: modify docker-compose.yml memory limits
```

**Slow startup**
```bash
# Model downloads on first run (~80MB)
# Use pre-built Docker image or run download_model.py separately
# Subsequent starts are faster due to model caching
```

**File upload issues**
```bash
# Ensure proper file permissions in data/ folder
sudo chmod 755 data/
# Check file format matches expected columns
```

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Considerations

- **Data Privacy**: All processing happens locally, no external API calls
- **Network**: Application binds to 0.0.0.0:8080 (configure firewall as needed)
- **Dependencies**: Regular updates recommended for security patches

## 📈 Future Enhancements

- [ ] Context-aware conversations
- [ ] Multi-Data type support
- [ ] Integration with Confluence API
- [ ] FAQ integrated

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Add comprehensive comments to new code
4. Test with sample data
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check troubleshooting section above
2. Review application logs
3. Verify data format and file permissions
4. Create GitHub issue with detailed description

---

# 🏗️ Detailed Architecture Guide

## 🔧 Core Components

### DataLoader (`core/data_loader.py`)
- Handles loading Excel/CSV files
- Validates data structure
- Cleans and preprocesses data
- Combines multiple data sources

### SearchEngine (`core/search_engine.py`)
- Manages sentence transformer models
- Creates embeddings for semantic search
- Supports pluggable search strategies
- Handles search operations

### SearchStrategies (`core/search_strategies.py`)
- Abstract base class for search algorithms
- `CosineSimilarityStrategy`: Standard cosine similarity
- `WeightedSimilarityStrategy`: Weighted field importance
- Extensible for custom search algorithms

### ResultFormatter (`core/formatter.py`)
- Formats search results for display
- Handles no-results scenarios
- Creates status messages

### ChatbotService (`core/chatbot_service.py`)
- Main orchestrator class
- Coordinates all components
- Provides high-level API

### Factory (`core/factory.py`)
- Creates component instances
- Supports dependency injection
- Enables easy testing and extension

## 🎨 UI Components

### ChatInterface (`ui/interface.py`)
- Gradio UI components
- Event handling
- User interaction management

### Styles (`ui/styles.py`)
- CSS styling definitions
- Centralized theme management

## ⚙️ Configuration

### Config (`config.py`)
- Centralized configuration management
- Type-safe configuration classes
- Environment-specific settings

```python
@dataclass
class AppConfig:
    search: SearchConfig
    data: DataConfig
    ui: UIConfig
```

## 🚀 Usage

### Basic Usage
```python
from main import main
main()
```

### Custom Configuration
```python
from core.chatbot_service import ChatbotService
from config import AppConfig, SearchConfig

# Custom configuration
config = AppConfig()
config.search.similarity_threshold = 0.2
config.search.max_results = 10

# Initialize service
service = ChatbotService(config)
```

### Custom Search Strategy
```python
from core.search_strategies import WeightedSimilarityStrategy
from core.factory import ComponentFactory

# Create custom strategy
strategy = WeightedSimilarityStrategy(
    tool_weight=3.0,
    action_weight=2.0,
    summary_weight=1.0
)

# Create search engine with custom strategy
search_engine = ComponentFactory.create_search_engine(
    config.search, 
    strategy
)
```

## 🔌 Extensibility

### Adding New Search Strategies

1. Create a new strategy class:
```python
class CustomSearchStrategy(SearchStrategy):
    def search(self, query_embedding, data_embeddings, data, top_k, threshold):
        # Your custom search logic
        return results
```

2. Register in factory:
```python
class SearchStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str, **kwargs):
        if strategy_type == "custom":
            return CustomSearchStrategy(**kwargs)
        # ... existing strategies
```

### Adding New Data Sources

1. Extend DataLoader:
```python
class CustomDataLoader(DataLoader):
    def _load_single_file(self, file_path: str):
        # Custom file loading logic
        pass
```

2. Use in service:
```python
service = ChatbotService()
service.data_loader = CustomDataLoader(config.data)
```

### Adding New UI Components

1. Create new UI module:
```python
# ui/custom_interface.py
class CustomInterface:
    def create_interface(self):
        # Custom UI logic
        pass
```

2. Use in main:
```python
from ui.custom_interface import CustomInterface

interface = CustomInterface(service, config.ui)
```

## 🧪 Testing

The modular structure enables easy unit testing:

```python
# Test data loader
def test_data_loader():
    config = DataConfig(data_folder="test_data")
    loader = DataLoader(config)
    data = loader.load_files()
    assert data is not None

# Test search engine
def test_search_engine():
    config = SearchConfig()
    engine = SearchEngine(config)
    # Mock data and test search
```

## 📈 Benefits

1. **Separation of Concerns**: Each module has a single responsibility
2. **Testability**: Components can be tested in isolation
3. **Extensibility**: Easy to add new features without breaking existing code
4. **Maintainability**: Clear structure makes code easier to understand and modify
5. **Reusability**: Components can be reused in different contexts
6. **Configuration Management**: Centralized settings for easy deployment

## 🛠️ Development Workflow

1. **Core Logic**: Implement business logic in `core/` modules
2. **UI Changes**: Modify `ui/` components for interface updates  
3. **Configuration**: Update `config.py` for new settings
4. **Extensions**: Use strategy pattern and factories for new features
5. **Testing**: Write unit tests for individual components