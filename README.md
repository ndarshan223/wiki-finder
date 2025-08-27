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
python app.py
```

### Option 2: Docker Setup
```bash
# Build and run with resource constraints
docker-compose up --build

# Access at http://localhost:8080
```

## 📊 Data Format

Place Excel (.xlsx) or CSV files in the `data/` folder with these columns:

| Column | Description | Example |
|--------|-------------|---------|
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
├── app.py                 # Main application with Gradio UI
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
├── download_model.py     # Pre-download sentence transformer
├── run_local.sh         # Local setup script
├── .dockerignore        # Docker build optimization
├── data/                # Data files directory
│   └── sdlc_tools_data.csv  # Sample data
└── README.md            # This file
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

### Adding New Data
1. Place Excel/CSV files in `data/` folder
2. Ensure proper column format (Tool, Action, Summary, Confluence Link)
3. Restart application to reload data

### Customizing Search
- **Similarity threshold**: Modify `similarities[idx] > 0.1` in `search()` method
- **Result count**: Change `top_k=5` parameter
- **Model**: Replace `'all-MiniLM-L6-v2'` with other sentence transformer models

### Performance Tuning
- **Memory**: Adjust Docker memory limits in `docker-compose.yml`
- **Batch size**: Modify embedding generation for large datasets
- **Caching**: Models are cached locally after first download

## 🐛 Troubleshooting

### Common Issues

**No data loaded**
```bash
# Check data folder
ls -la data/
# Ensure CSV/Excel files have correct columns
```

**Memory errors**
```bash
# Reduce Docker memory limits or use smaller model
# Check available system memory
free -h
```

**Slow startup**
```bash
# Model downloads on first run
# Use pre-built Docker image or download_model.py
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