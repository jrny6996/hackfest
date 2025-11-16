# Python base image
FROM python:3.12-slim

# Node.js + npm for Tailwind
# (Debian-based commands work on python:slim images)
RUN apt-get update && apt-get install -y curl gcc build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm --version \
    && node --version \
    && apt-get clean

# Create working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies, including:
# django-tailwind[cookiecutter,honcho,reload]
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django dev server port
EXPOSE 8000

# Install Tailwind dependencies (node_modules)
# NOTE: This must run after your project is copied,
# and AFTER `tailwind init` has created the theme app.
RUN python manage.py tailwind install || true

# Default command — run Tailwind + Django together
CMD ["python", "manage.py", "tailwind", "dev"]
