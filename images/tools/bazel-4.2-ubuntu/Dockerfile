FROM registry.gitlab.com/ownport/docker-images/base:21.04-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
