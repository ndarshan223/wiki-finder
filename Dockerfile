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
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
# This allows pip install to be cached if requirements don't change
COPY requirements.txt .

# Install Python dependencies to a specific target directory
# --no-cache-dir: Don't cache pip packages to reduce image size
# --target: Install packages to specific directory for copying to runtime stage
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

# Pre-download the sentence transformer model during build
# This improves startup time and enables offline usage
COPY download_model.py .
ENV PYTHONPATH=/build/deps
RUN python download_model.py

# Stage 2: Runtime - Clean image with only necessary components
# Use Python 3.9 slim image for smaller size and security
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy only the installed dependencies from builder stage
# This excludes build tools and reduces final image size
COPY --from=builder /build/deps /usr/local/lib/python3.9/site-packages/
COPY --from=builder /build/models ./models/

# Copy application files to container
COPY app.py sample_data.py ./

# Create necessary directories for data
# /app/data: For SDLC tools data files (Excel/CSV)
RUN mkdir -p /app/data

# Set environment variables for better Python behavior in containers
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port 8080
EXPOSE 8080

# Run the application
# Use python instead of python3 since we're in a Python container
CMD ["python", "app.py"]