ARG BASE_IMAGE=nowcasting-base:latest
FROM ${BASE_IMAGE}

WORKDIR /opt/project
ENV PYTHONPATH=/opt/project

COPY requirements/ /opt/project/requirements
RUN pip install --no-cache-dir -r requirements/track.txt

COPY . /opt/project

CMD ["bash"]