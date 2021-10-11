ARG BRANCH=${BRANCH}

FROM gcr.io/kaniko-project/executor:v1.6.0 as kaniko_binary

FROM registry.gitlab.com/ownport/docker-images/${BRANCH}/base:20.10-ubuntu

COPY assets/ /tmp/assets/

RUN echo '[INFO] Configure environment' && \
        /tmp/assets/bin/install.sh 

COPY --from=kaniko_binary /kaniko/executor /usr/local/bin/
COPY --from=kaniko_binary /kaniko/ssl/certs/* /kaniko/ssl/certs/
