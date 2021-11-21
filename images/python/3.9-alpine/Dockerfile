ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/base:3.14-alpine${BRANCH}

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
