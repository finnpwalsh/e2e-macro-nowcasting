# immutable / invariant
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# runtime behavior
CMD ["python", "scripts/ingest_fred.py"]