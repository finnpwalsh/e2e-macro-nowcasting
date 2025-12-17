# immutable / invariant
FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --noc-cache-dir -r /app/requirements.txt

# runtime behavior
CMD["python", "scripts/ingest_fred.py"]