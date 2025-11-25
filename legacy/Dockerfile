FROM python:3.14-slim

# System-Dependencies
RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Python-Dependencies
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Port freigeben
EXPOSE 8000

# Entwicklungsmodus mit Hot-Reload
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
