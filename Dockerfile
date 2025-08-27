# Use Python 3.9 slim image for smaller size and security
# Slim images contain only essential packages
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies required for Python packages
# gcc: Required for compiling some Python packages (numpy, scipy)
# Clean apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
# This allows pip install to be cached if requirements don't change
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't cache pip packages to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files to container
COPY . .

# Create necessary directories for data and models
# /app/data: For SDLC tools data files (Excel/CSV)
# /app/models: For cached sentence transformer models
RUN mkdir -p /app/data /app/models

# Pre-download the sentence transformer model during build
# This improves startup time and enables offline usage
# Requires internet connection during docker build
RUN python download_model.py

# Expose port 8080 (standard Gradio port)
EXPOSE 8080

# Set environment variables for better Python behavior in containers
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
# Use python instead of python3 since we're in a Python container
CMD ["python", "app.py"]