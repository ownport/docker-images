ARG TAG_SUFFIX=${TAG_SUFFIX}

FROM gcr.io/kaniko-project/executor:v1.7.0-debug as kaniko_binary

FROM busybox:1.34.1

COPY assets/ /tmp/assets/

RUN echo "[INFO] Create kaniko directory structure" && \
        mkdir -p /kaniko/ssl/certs && \
    echo "[INFO] Install update-docker-config.sh script" && \
        mv /tmp/assets/bin/update-docker-config.sh /kaniko


COPY --from=kaniko_binary /kaniko/executor /kaniko
COPY --from=kaniko_binary /kaniko/ssl/certs/* /kaniko/ssl/certs/
COPY --from=kaniko_binary /etc/nsswitch.conf /etc/nsswitch.conf

ENV SSL_CERT_DIR=/kaniko/ssl/certs
ENV DOCKER_CONFIG /kaniko/.docker/
