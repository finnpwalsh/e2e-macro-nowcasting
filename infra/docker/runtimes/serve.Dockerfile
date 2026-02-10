ARG BASE_IMAGE=nowcasting-base:latest
FROM ${BASE_IMAGE}

WORKDIR /opt/project

# stage-specific deps
COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir -r requirements/runtimes/serve.txt

# install repo
COPY . /opt/project
RUN pip install --no-cache-dir .

EXPOSE 8000

# Run FastAPI via installed package
CMD ["uvicorn", "src.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]