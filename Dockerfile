# Use a slim Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install system dependencies (required for spaCy and clean builds)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Set environment vars
ENV PYTHONUNBUFFERED=1

# Command to run Pizza
CMD ["python", "src/main.py"]
