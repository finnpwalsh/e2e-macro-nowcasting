FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/project
ENV PYTHONPATH=/opt/project

COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/serve.txt

COPY . /opt/project

EXPOSE 8000

CMD ["uvicorn", "src.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]