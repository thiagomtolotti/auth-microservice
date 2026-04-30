FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the bin folder is in the PATH
ENV PATH="/usr/local/bin:$PATH"

CMD ["fastapi", "dev", "--host", "0.0.0.0"]