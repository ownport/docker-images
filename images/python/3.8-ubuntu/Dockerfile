FROM ownport/base:20.04-ubuntu

COPY assets/ /tmp/assets/

RUN echo "[INFO] Install deploy-utils script" && \
        mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \
    echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
