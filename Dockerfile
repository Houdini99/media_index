# We use a lightweight Python base image
FROM python:3.11-slim

# Install FFmpeg (required for your moviepy video thumbnails)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your complete code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Launch the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
