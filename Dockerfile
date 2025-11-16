FROM python:3.12-slim

# Install system deps + Node.js (required for tailwind)
RUN apt-get update && apt-get install -y curl gcc build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Workdir
WORKDIR /app

# Copy requirements early to leverage Docker cache
COPY requirements.txt .

# Install Python deps (including django-tailwind)
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Install Tailwind CSS dependencies (must run after theme/ exists)
RUN python manage.py tailwind install || true

# Expose Django port
EXPOSE 8000

# Run tailwind + django dev servers
CMD ["python", "manage.py", "tailwind", "dev"]
