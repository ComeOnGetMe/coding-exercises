# Use Python 3.12 slim Linux image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install just to /usr/local/bin (which is in PATH)
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# Install uv to /usr/local/bin (which is in PATH)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files for uv
COPY pyproject.toml uv.lock ./

# Copy justfile
COPY justfile ./

# Copy source code
COPY src/ ./src/

# Expose the port the service runs on
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV PYTHONPATH=/app

# Command to start the service using just
CMD ["just", "start"]

