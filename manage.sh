#!/usr/bin/env bash

set -eu

case ${1} in
    help)
        echo 'Available options:'
        echo ' update-base-images   - update base images: alpine, ubuntu, ..'
        echo ' build                - build docker images'
        echo ' console              - run console for specific image'
        ;;
    update-base-images)
        echo "[INFO] Updating base images" && \
            docker pull alpine:3.12
            docker pull alpine:3.13
            docker pull ubuntu:20.04
            docker pull ubuntu:20.10
        ;;
    build)
        shift
        DOCKERFILE_PATH=${1:-}

        [ -z "${DOCKERFILE_PATH}" ] && {
            echo "[ERROR] Please specify the image name by 'image' parameter"
            exit 1
        } || {
            echo "[INFO] Building image: ${DOCKERFILE_PATH}"
            cd ${DOCKERFILE_PATH}
            source metadata
            docker build -t ownport/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION} .
        }
        ;;
    console)
        shift
        DOCKERFILE_PATH=${1:-}

        [ -z "${DOCKERFILE_PATH}" ] && {
            echo "[ERROR] Please specify the path to Dockerfile"
            exit 1
        } || {
            echo "[INFO] Running console for image: ${DOCKERFILE_PATH}"
            cd ${DOCKERFILE_PATH}
            source metadata
            echo "[INFO] The image: ownport/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}, the container name: ${DOCKER_IMAGE_NAME}-console"
            docker run -ti --rm --name ${DOCKER_IMAGE_NAME}-console \
                ownport/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION} \
                ${DOCKER_IMAGE_SHELL}
        }
        ;;
    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No arguments specified, use help for more details" 
        else
            exec "$@"
        fi
        ;;
esac 


