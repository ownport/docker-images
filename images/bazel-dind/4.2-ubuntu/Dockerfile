ARG BRANCH=${BRANCH}
FROM registry.gitlab.com/ownport/docker-images/${BRANCH}/bazel:4.2-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
