# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (החלף את main.py בשם הסקריפט שלך כשהיה מוכן)
CMD ["python", "app/main.py"]
