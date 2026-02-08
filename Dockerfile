# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (if needed for dashboard or API)
EXPOSE 8000

# Default command
CMD ["python", "orchestrator.py"]
# Use a slim Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi \
    && if [ -f requirements-dev.txt ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Debugging step to verify environment setup
RUN echo "PYTHONPATH: $PYTHONPATH" && ls -la /app

# Default command to run tests
CMD ["pytest"]
