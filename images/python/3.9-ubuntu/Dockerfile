ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/base:21.04-ubuntu${BRANCH}

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
