ARG TAG_SUFFIX=${TAG_SUFFIX}
FROM registry.gitlab.com/ownport/docker-images/python:3.9-ubuntu${TAG_SUFFIX}

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
