FROM gcr.io/kaniko-project/executor:v1.6.0-debug as kaniko_binary

FROM busybox:1.34.1 as target

ENV SSL_CERT_DIR=/kaniko/ssl/certs
ENV DOCKER_CONFIG /kaniko/.docker/

COPY assets/ /tmp/assets/

RUN echo "[INFO] Preparing data for copying" && \
        mkdir -p \
            /kaniko \
            /kaniko/.docker \
            /kaniko/ssl/certs

COPY --from=kaniko_binary /kaniko/executor /kaniko
COPY --from=kaniko_binary /kaniko/ssl/certs/* /kaniko/ssl/certs
COPY --from=kaniko_binary /etc/nsswitch.conf /etc/nsswitch.conf

RUN echo "[INFO] Install update-docker-config.sh script" && \
        mv /tmp/assets/bin/update-docker-config.sh /kaniko && \
    /tmp/assets/tests/smoke-tests.sh
