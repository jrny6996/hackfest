FROM python:3.12-slim

# Install system deps + Node.js
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    build-essential \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Create work directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install Tailwind dependencies, but DO NOT fail if theme isn't ready
# RUN python manage.py tailwind install || echo "⚠️ Tailwind install skipped"

# Expose Django dev port
EXPOSE 8000

# Run Tailwind watcher + Django server together
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
