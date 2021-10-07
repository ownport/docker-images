ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/${BRANCH}/base:20.10-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
