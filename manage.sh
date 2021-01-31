#!/usr/bin/env bash

set -eu
# GitLab Docker Registry
GITLAB_DOCKER_REGISTRY="registry.gitlab.com"
# GitLab Group
GITLAB_GROUP=ownport
# GitLab Project
GITLAB_PROJECT=docker-images


case ${1} in
    help)
        echo 'Available options:'
        echo ' update-base-images       - update base images: alpine, ubuntu, ..'
        echo ' build                    - build docker image'
        echo ' test                     - run tests for docker image'
        echo ' remove                   - remove docker image'
        echo ' publish-to-gl-registry   - publish docker image to GitLab Registry'
        echo ' console                  - run console for specific image'
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

            # Set GitLab Docker Image
            GITLAB_DOCKER_IMAGE=${GITLAB_DOCKER_REGISTRY}/${GITLAB_GROUP}/${GITLAB_PROJECT}/${DOCKER_IMAGE_NAME}
            
            # Use Docker caching
            docker pull ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} || true
    
            # Build docker image
            docker build --cache-from ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} \
                --tag ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} .
        }
        ;;
    test)
        shift
        DOCKERFILE_PATH=${1:-}

        [ -z "${DOCKERFILE_PATH}" ] && {
            echo "[ERROR] Please specify the image name by 'image' parameter"
            exit 1
        } || {
            echo "[INFO] Tesing image from directory: ${DOCKERFILE_PATH}"
            cd ${DOCKERFILE_PATH}
            source metadata

            # Set GitLab Docker Image
            GITLAB_DOCKER_IMAGE=${GITLAB_DOCKER_REGISTRY}/${GITLAB_GROUP}/${GITLAB_PROJECT}/${DOCKER_IMAGE_NAME}

            echo "[INFO] GitLab Docker Image: ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION}"

            # Run tests for docker image
            docker run --rm -v "$(pwd)/tests":/tests \
		            ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} /tests/run-tests.sh
        }
        ;;
    remove)
        shift
        DOCKERFILE_PATH=${1:-}

        [ -z "${DOCKERFILE_PATH}" ] && {
            echo "[ERROR] Please specify the image name by 'image' parameter"
            exit 1
        } || {
            echo "[INFO] Removing image from path: ${DOCKERFILE_PATH}"
            cd ${DOCKERFILE_PATH}
            source metadata

            # Set GitLab Docker Image
            GITLAB_DOCKER_IMAGE=${GITLAB_DOCKER_REGISTRY}/${GITLAB_GROUP}/${GITLAB_PROJECT}/${DOCKER_IMAGE_NAME}

            # Remove docker images
            docker image rm ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} ${GITLAB_DOCKER_IMAGE}:latest
        }
        ;;
    publish-to-gitlab-registry)
        shift
        DOCKERFILE_PATH=${1:-}

        [ -z "${DOCKERFILE_PATH}" ] && {
            echo "[ERROR] Please specify the image name by 'image' parameter"
            exit 1
        } || {
            echo "[INFO] Publish image from path: ${DOCKERFILE_PATH} to GitLab Registry: ${GITLAB_DOCKER_REGISTRY}"
            cd ${DOCKERFILE_PATH}
            source metadata

            # Set GitLab Docker Image
            GITLAB_DOCKER_IMAGE=${GITLAB_DOCKER_REGISTRY}/${GITLAB_GROUP}/${GITLAB_PROJECT}/${DOCKER_IMAGE_NAME}

            # Push docker image(-s) to GitLab Docker Registry
            docker push ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} 
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

            # Set GitLab Docker Image
            GITLAB_DOCKER_IMAGE=${GITLAB_DOCKER_REGISTRY}/${GITLAB_GROUP}/${GITLAB_PROJECT}/${DOCKER_IMAGE_NAME}

            echo "[INFO] The image: ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION}, the container name: ${DOCKER_IMAGE_NAME}-console"

            # Open console
            docker run -ti --rm --name ${DOCKER_IMAGE_NAME}-console \
                ${GITLAB_DOCKER_IMAGE}:${DOCKER_IMAGE_VERSION} \
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
