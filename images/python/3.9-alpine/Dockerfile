FROM registry.gitlab.com/ownport/docker-images/base:3.14-alpine

COPY assets/ /tmp/assets/

RUN echo "[INFO] Install py3-utils script" && \
        mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \
    echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
