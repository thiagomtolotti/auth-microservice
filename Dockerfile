FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the bin folder is in the PATH
ENV PATH="/usr/local/bin:$PATH"

CMD ["fastapi", "dev", "--host", "0.0.0.0"]