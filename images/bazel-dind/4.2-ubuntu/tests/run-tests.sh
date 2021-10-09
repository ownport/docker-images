#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out bazel version' && \
    bazel --version

echo '[TEST] Check dockerd version' && \
    dockerd --version

echo '[TEST] Check docker version' && \
    docker --version

echo '[TEST] Check if dind script is available' && {
    DIND_PATH="/usr/local/bin/dind"
    if [ -f ${DIND_PATH} ]
    then
        echo "The file ${DIND_PATH} exists"
    else
        echo "[ERROR] The file ${DIND_PATH} does not exist"
        exit 1
    fi  
} 
