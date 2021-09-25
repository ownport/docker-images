FROM registry.gitlab.com/ownport/docker-images/bazel:4.2-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
