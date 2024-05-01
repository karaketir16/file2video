# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the Docker image
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libzbar0 \
    ffmpeg \
    git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Clone the repository
RUN git clone --depth 1 --branch master https://github.com/karaketir16/file2video.git /app

# Copy the current directory contents into the container at /app
#COPY . /app

RUN uv venv

# Install any needed packages specified in requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt

WORKDIR /data

# Run file2video.py when the container launches
ENTRYPOINT ["/app/.venv/bin/python", "/app/file2video.py", "--docker"]
CMD []
