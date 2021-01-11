FROM ownport/base:3.12-alpine

COPY assets/ /tmp/assets/

RUN echo "[INFO] Install py3-utils script" && \
        mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \
    echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
