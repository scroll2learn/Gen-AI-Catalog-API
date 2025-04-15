# Pull official base image
FROM python:3.11-slim-buster

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql postgresql-server-dev-all git make \
  && apt-get clean

# Install pgvector extension
RUN git clone --branch v0.4.0 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make && make install \
    && rm -rf /tmp/pgvector

# Set up Git credentials
ARG TOKEN
RUN git config --global url."https://${TOKEN}@github.com/".insteadOf "https://github.com/"

# Clone and install bh-cluster-utils
RUN git clone https://github.com/bh-ai/bh-cluster-utils.git /usr/src/bh-cluster-utils
RUN pip install --no-cache-dir -e /usr/src/bh-cluster-utils  # Install bh-cluster-utils properly

# Copy application files first
COPY . /usr/src/app

# Install Python dependencies for catalog API
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Python path
ENV PYTHONPATH="/usr/src/app"

# Ensure start.sh is executable
RUN chmod +x /usr/src/app/start.sh

# Expose necessary ports
EXPOSE 8011
EXPOSE 8088

# Use the start script as the entry point
CMD ["/bin/bash", "/usr/src/app/start.sh"]
