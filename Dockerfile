# Use official slim Python image
FROM python:3.10-slim

# Expose the port your app will run on
EXPOSE 5000

# Set working directory
WORKDIR /app

# Environment
ENV POETRY_VERSION=1.3.2
# Note: Force pip to use pre-built wheels
ENV PIP_ONLY_BINARY=:all:

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Copy source code and config
COPY apis ./apis
COPY model ./model
COPY core ./core
COPY modules ./modules
COPY app.py config.py caching.py ./
# Copy database/migration setup
COPY alembic ./alembic
COPY alembic.ini .
# Copy runtime entrypoint
COPY entrypoint.sh .
COPY alembic alembic.ini ./
COPY entrypoint.sh ./

# Setup Entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
