FROM apache/airflow:2.9.3-python3.11

WORKDIR /opt/project

COPY requirements/ /opt/project/requirements/

USER airflow
RUN pip install --no-cache-dir -r requirements/airflow.txt

COPY . /opt/project

ENV PYTHONPATH=/opt/project/

USER airflow