#!/bin/sh

set -eu


case ${1} in
    help)
        echo 'Available options:'
        echo ' update               - update Alpine packages list'
        echo ' install              - install packages'
        echo ' install-build-deps   - install build deps'
        echo ' add-user-and-group   - add user and group'
        echo ' cleanup              - cleanup'
        ;;
    update)
        echo "[INFO] Update apk index" && \
            apk update
        ;;
    install)
        shift
        echo "[INFO] Installing the packages: $@" && \
            apk add --no-cache $@
        ;;
    install-build-deps)
        shift
        echo "[INFO] Installing the packages: $@" && \
            apk add --no-cache --virtual .build-deps $@
        ;;
    add-user-and-group)
        shift
        USER_ID=${1:-}
        USER_NAME=${2:-}
        GROUP_ID=${3:-}
        GROUP_NAME=${4:-}   
        echo "[INFO] Add user and group, user id/name: ${USER_NAME}/${USER_ID}, group id/name: ${GROUP_ID}/${GROUP_NAME}" && \
            addgroup -g ${GROUP_ID} ${GROUP_NAME} && \
            adduser -u ${USER_ID} -G ${GROUP_NAME} -s /bin/sh -D ${USER_NAME}
        ;;
    cleanup)
        echo "[INFO] Remove apt index" && \
            rm -rf \
                /var/lib/apt/lists/* \
                /tmp/*
        echo "[INFO] Removing build deps" && \
            apk del .build-deps || echo "[WARNING] No .build-deps packages"
        ;;
    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No arguments specified, use help for more details" 
        else
            exec "$@"
        fi
        ;;
esac 

