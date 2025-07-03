FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app/

# Install system dependencies required to build numpy and psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app/main.py"]
