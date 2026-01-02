FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Install psycopg2 dependencies
RUN pip install psycopg2-binary

# Copy the rest of the application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run the application
CMD ["python", "bot.py"]