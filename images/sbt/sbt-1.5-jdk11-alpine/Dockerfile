FROM registry.gitlab.com/ownport/docker-images/openjdk:11-jdk-alpine

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
