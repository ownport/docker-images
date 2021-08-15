FROM registry.gitlab.com/ownport/docker-images/base:3.14-alpine

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh
