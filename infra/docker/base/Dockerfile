# immutable / invariant
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/project

# dependencies
COPY dependencies/ /opt/project/dependencies/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r dependencies/base.txt

# runtime behavior
CMD ["bash"]