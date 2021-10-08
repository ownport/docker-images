ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/${BRANCH}/kaniko:1.6-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
