ARG BASE_IMAGE=nowcasting-dev-base:latest
FROM ${BASE_IMAGE}

WORKDIR /opt/project

# stage-specific deps
COPY dependencies/ /opt/project/dependencies/
RUN pip install --no-cache-dir -r dependencies/runtimes/train.txt

# install repo
COPY . /opt/project
RUN pip install --no-cache-dir .

CMD ["bash"]