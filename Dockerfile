# Stage 1: Base
FROM python:3.12-slim AS base
RUN apt-get update && apt-get install -y build-essential python3-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Stage 3: Development
FROM base AS development

RUN uv sync --frozen --no-cache --group dev

COPY . .