FROM gcr.io/kaniko-project/executor:v1.7.0-debug as kaniko_binary

COPY assets/ /tmp/assets/

RUN /kaniko/executor version && \
    echo "[INFO] Preparing data for copying" && \
        mkdir -p \
            /tmp/etc \
            /tmp/kaniko \
            /tmp/kaniko/.docker \
            /tmp/kaniko/ssl/certs && \
    echo "[INFO] Copying kaniko files" && \
        cp /kaniko/executor /tmp/kaniko && \
        cp /kaniko/ssl/certs/* /tmp/kaniko/ssl/certs/ && \
    echo "[INFO] Install update-docker-config.sh script" && \
        mv /tmp/assets/bin/update-docker-config.sh /kaniko

FROM busybox:1.34.1 as target

RUN ls /kaniko

ENV SSL_CERT_DIR=/kaniko/ssl/certs
ENV DOCKER_CONFIG /kaniko/.docker/

COPY --from=kaniko_binary /tmp/kaniko /kaniko
COPY --from=kaniko_binary /etc/nsswitch.conf /etc/nsswitch.conf
COPY assets/ /tmp/assets/

RUN /tmp/assets/tests/smoke-tests.sh
