FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (ignoring .env if it doesn't exist)
COPY app.py .
COPY init_db.py .
COPY .env* .
COPY templates/ templates/
COPY static/ static/

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5001

# Initialize database and start app
CMD ["sh", "-c", "python init_db.py && python app.py"]
