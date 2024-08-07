# Base image for building the application
FROM python:3.12.0-slim-bullseye as base

# Install system dependencies and remove cache to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Set the working directory
WORKDIR /app/src

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install production dependencies
RUN poetry install --only main --no-root

# Remove development tools to reduce image size
RUN apt-get purge -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY deploy .

# Install the project itself
RUN poetry install --only main

# Set the command to run the application
CMD ["/usr/local/bin/python", "-m", "product_fusion_backend"]

# Development stage
FROM base as dev

# Expose the application port (if required)
EXPOSE 8000
