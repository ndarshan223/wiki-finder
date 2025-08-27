# Semantic Search Chatbot - Setup Instructions

## Quick Start (Local)

### Prerequisites
- Python 3.9+
- 2GB+ available RAM

### Option 1: Direct Python Setup
```bash
# Clone/navigate to project directory
cd chatbot

# Run setup script
./run_local.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create sample data
python sample_data.py

# Run application
python app.py
```

Access at: http://localhost:7860

## Docker Setup (Recommended for <4GB RAM)

### Prerequisites
- Docker & Docker Compose
- 3GB+ available RAM

### Run with Docker
```bash
# Build and start
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

Access at: http://localhost:7860

### Memory Management
The Docker setup is configured with:
- Memory limit: 3GB
- Memory reservation: 1GB

## Usage

1. **Load Data**: Go to "Data Management" tab and upload your Excel file
2. **Search**: Use the "Chat" tab to query your data
3. **Query Examples**:
   - "How to setup GitLab CI/CD?"
   - "SonarQube configuration"
   - "Nexus repository management"

## File Structure
```
chatbot/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
├── sample_data.py     # Sample data generator
├── run_local.sh       # Local setup script
└── data/              # Data directory
    └── sample_tools_data.xlsx
```

## Excel File Format
Your Excel file should have these columns:
- **Tool**: Name of the tool (GitLab, SonarQube, etc.)
- **Action**: What action/task
- **Summary**: Description of the content
- **Confluence Link**: Link to documentation

## Troubleshooting

### Low Memory Issues
- Use Docker setup with memory limits
- Close other applications
- Reduce batch size in semantic search

### Port Conflicts
Change port in docker-compose.yml:
```yaml
ports:
  - "8080:7860"  # Use port 8080 instead
```