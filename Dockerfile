FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for headless execution
ENV HEADLESS=true

# Default entrypoint - can be overridden
ENTRYPOINT ["python", "-m", "pytest"]

