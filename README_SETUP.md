# Semantic Search Chatbot - Setup Instructions

## Files Created
- `app.py` - Main application with Gradio UI and semantic search
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Docker compose with resource limits
- `sdlc_tools_data.csv` - Sample data (move to data/ folder)

## Setup Instructions

### 1. Prepare Data
```bash
# Move the sample data to data folder (requires proper permissions)
sudo mv sdlc_tools_data.csv data/
# OR create your own Excel file with columns: Tool, Action, Summary, Confluence Link
```

### 2. Run Locally (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### 3. Run with Docker
```bash
# Build and run with resource constraints
docker-compose up --build
```

### 4. Access Application
- Open browser: http://localhost:7860
- Upload Excel/CSV file in "Data Management" tab
- Use "Chat" tab for semantic search

## Resource Requirements
- Memory: <3GB RAM
- CPU: Minimal (sentence transformer model is lightweight)
- Storage: ~500MB for dependencies

## Data Format
CSV/Excel with columns:
- Tool: SDLC tool name
- Action: What action/task
- Summary: Description
- Confluence Link: Documentation URL

## Features
- Semantic search using sentence transformers
- Gradio chat interface
- In-memory vector database
- Docker support with resource limits
- Support for Excel and CSV files