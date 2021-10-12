ARG BRANCH=${BRANCH}

FROM gcr.io/kaniko-project/executor:v1.6.0-debug as kaniko_binary

FROM busybox:1.34.0

RUN mkdir -p /kaniko/ssl/certs

COPY --from=kaniko_binary /kaniko/executor /kaniko
COPY --from=kaniko_binary /kaniko/ssl/certs/* /kaniko/ssl/certs/
COPY --from=kaniko_binary /etc/nsswitch.conf /etc/nsswitch.conf

ENV SSL_CERT_DIR=/kaniko/ssl/certs
ENV DOCKER_CONFIG /kaniko/.docker/
