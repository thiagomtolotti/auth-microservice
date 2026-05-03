# Stage 1: Base
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y build-essential python3-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Testing
FROM base AS testing

RUN pip install pytest-watch 

CMD ["pytest-watch"]

# Stage 3: Development
FROM base AS development
CMD ["fastapi", "dev", "--host", "0.0.0.0"]

# Stage 4: Coverage
FROM testing AS coverage

RUN pip install pytest pytest-cov

CMD ["pytest", "--cov=app", "--cov-report=html"]