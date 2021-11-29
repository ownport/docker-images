ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/openjdk:8-jdk-ubuntu${BRANCH}

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
