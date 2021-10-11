ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/${BRANCH}/base:3.14-alpine

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 

USER podman
