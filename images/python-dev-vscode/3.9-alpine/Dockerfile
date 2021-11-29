ARG TAG_SUFFIX=${TAG_SUFFIX}
FROM registry.gitlab.com/ownport/docker-images/python-dev:3.9-alpine${TAG_SUFFIX}

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 

USER vscode
