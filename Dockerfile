FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bind the entire application directory to the container
COPY . /app

# Copy the .env file to the container
COPY .env .

# Define a named volume for logs
VOLUME /app/logs

EXPOSE 5001

CMD ["python", "app.py"]