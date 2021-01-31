#!/bin/sh

set -eu

OPTION=${1:-help}

case ${OPTION} in
    help)
        cat << EOM
Usage: deploy-utils.sh <option> [arguments]

Available options:
    update              - update Alpine packages list
    install             - install packages
                                args: 
                                - <packages>:   list packages
    install-build-deps  - install build deps
                                args:
                                - <packages>:   list packages   
    add-user-and-group  - add user and group
                                args:
                                - <user_id>:    user id
                                - <username>:   username
                                - <group_id>:   group id
                                - <groupname>:  group name
                                - <shell_path>: shell path, default: /bin/sh
    cleanup             - cleanup
EOM
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
        SHELL_PATH=${5:-/bin/sh}
        echo "[INFO] Add user and group, user id/name: ${USER_NAME}/${USER_ID}, group id/name: ${GROUP_ID}/${GROUP_NAME}" && \
            addgroup -g ${GROUP_ID} ${GROUP_NAME} && \
            adduser -u ${USER_ID} -G ${GROUP_NAME} -s $SHELL_PATH -D ${USER_NAME}

        # Add sudo support for non-root user
        if [ "${USER_NAME}" != "root" ]; then
            mkdir -p /etc/sudoers.d/
            echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME
            chmod 0440 /etc/sudoers.d/$USER_NAME
        fi
        ;;
    cleanup)
        echo "[INFO] Remove apt index" && \
            rm -rf \
                /var/lib/apt/lists/* \
                /tmp/*
        
        echo "[INFO] Removing build deps" && {
            BUILD_DEPS=$(apk info -q | grep .build-deps)
            if [ -z "${BUILD_DEPS}" ]; then
                echo "[WARNING] No .build-deps packages"
            else
                apk del .build-deps
            fi
        }
        ;;
    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No arguments specified, use 'help' for more details" 
        else
            exec "$@"
        fi
        ;;
esac 

