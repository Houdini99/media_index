# We use a lightweight Python base image
FROM python:3.11-slim

# Install FFmpeg (required for moviepy video thumbnails)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Install Python libraries (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY run.py ./
COPY app ./app

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5001

# Launch via the entry point (preserves StreamToLogger redirection
# and the LAN-IP startup banner)
CMD ["python", "run.py"]
