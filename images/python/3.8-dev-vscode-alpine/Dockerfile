FROM registry.gitlab.com/ownport/docker-images/python:3.8-dev-alpine

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 

USER vscode
