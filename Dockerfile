# Stage 1: Build environment and compile dependencies
FROM python:3.14-slim AS builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files, README, source code, and schemas
COPY pyproject.toml uv.lock README.md ./
COPY src/ src/
COPY schemas/ schemas/

# Install dependencies and build the package into a virtual environment
RUN uv sync --frozen --no-dev --no-editable

# Stage 2: Minimal runtime image
FROM python:3.14-slim AS runner

WORKDIR /app

# Install runtime librdkafka library
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment, source code, and schemas from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/schemas /app/schemas
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# Set environment path to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

ENTRYPOINT ["python", "-m", "pathogen_data_generator.producer"]