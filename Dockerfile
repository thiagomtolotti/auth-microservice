# Stage 1: Base
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y build-essential python3-dev

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir ".[dev]"

# Stage 2: Testing
FROM base AS testing-watch

RUN pip install pytest-watch 

COPY . .

CMD ["pytest-watch"]

FROM base as testing

COPY . .

ENTRYPOINT ["pytest"]
CMD ["."]

# Stage 3: Development
FROM base AS development

COPY . .

CMD ["fastapi", "dev", "--host", "0.0.0.0"]

# Stage 4: Coverage
FROM testing AS coverage

RUN pip install pytest pytest-cov

CMD ["--cov=app", "--cov-report=html"]