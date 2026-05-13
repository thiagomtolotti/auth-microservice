# Stage 1: Base
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y build-essential python3-dev

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir ".[dev]"


# Stage 3: Development
FROM base AS development

COPY . .

RUN pip install -e .

CMD ["fastapi", "dev", "--host", "0.0.0.0"]
