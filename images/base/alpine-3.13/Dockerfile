FROM alpine:3.13

COPY assets/ /tmp/assets/

RUN echo "[INFO] Install deploy-utils script" && \
        mv /tmp/assets/bin/deploy-utils.sh /usr/local/bin/ && \
    echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 
