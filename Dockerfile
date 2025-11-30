# Use official Python runtime as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files
ENV PYTHONUNBUFFERED 1         # Prevents Python from buffering stdout/stderr

# Set working directory in container
WORKDIR /app

# Install system dependencies
# mysql-connector-python needs these to compile
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project to container
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]