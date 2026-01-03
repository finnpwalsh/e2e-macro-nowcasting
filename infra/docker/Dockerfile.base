# immutable / invariant
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/project
ENV PYTHONPATH=/opt/project

# dependencies
COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/base.txt

# runtime behavior
CMD ["bash"]