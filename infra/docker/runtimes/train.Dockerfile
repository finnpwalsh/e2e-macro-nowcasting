ARG BASE_IMAGE=nowcasting-base:latest
FROM ${BASE_IMAGE}

WORKDIR /opt/project

# stage-specific deps
COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir -r requirements/runtimes/train.txt

# install repo
COPY . /opt/project
RUN pip install --no-cache-dir .

CMD ["bash"]