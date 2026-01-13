ARG BASE_IMAGE=nowcasting-base:latest
FROM ${BASE_IMAGE}

WORKDIR /opt/project
ENV PYTHONPATH=/opt/project

COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir -r requirements/serve.txt

COPY . /opt/project

EXPOSE 8000

CMD ["uvicorn", "src.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]