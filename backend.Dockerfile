# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable to ensure logs are visible
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for building gevent and other Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libev-dev \
    libffi-dev \
    python3-dev \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "appAPI:app", "--host", "0.0.0.0", "--port", "8000"]
