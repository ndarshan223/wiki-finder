# Multi-stage build to reduce image size by separating build and runtime dependencies
# This approach significantly reduces final image size while maintaining functionality

# Stage 1: Builder - Install dependencies and download models
# Use Python 3.9 slim image for smaller size and security
FROM python:3.9-slim as builder

# Set working directory for build stage
WORKDIR /build

# Install system dependencies required for Python packages
# gcc: Required for compiling some Python packages (numpy, scipy)
# g++: Additional compiler for C++ dependencies
# Clean apt cache to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
# This allows pip install to be cached if requirements don't change
COPY requirements.txt .

# Install Python dependencies using --user flag for proper isolation
# --no-cache-dir: Don't cache pip packages to reduce image size
# --user: Install packages to user directory for easy copying
RUN pip install --no-cache-dir --user -r requirements.txt

# Pre-download the sentence transformer model during build
# This improves startup time and enables offline usage
COPY download_model.py .
ENV PATH=/root/.local/bin:$PATH
RUN python download_model.py

# Stage 2: Runtime - Clean image with only necessary components
# Use Python 3.9 slim image for smaller size and security
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy only the installed dependencies from builder stage
# This excludes build tools and reduces final image size
COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/models ./models/

# Copy application files to container
COPY main.py app.py config.py ./
COPY core/ ./core/
COPY ui/ ./ui/

# Copy data files - CRITICAL: This was missing and caused the internal server error
# /app/data: For SDLC tools data files (Excel/CSV)
COPY data/ ./data/

# Set environment variables for better Python behavior in containers
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port 8080 for Gradio web interface
EXPOSE 8080

# Run the application
# Use python instead of python3 since we're in a Python container
CMD ["python", "main.py"]