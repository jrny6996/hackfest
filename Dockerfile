# Use official Python image
FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Install system dependencies (optional but common for Django + Pillow, psycopg, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Expose Django dev server port
EXPOSE 8000

# Default command — run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
