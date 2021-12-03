#!/bin/sh

set -e

echo "[INFO] Run tests"

echo "[TEST] Print out Kaniko version" && \
    /kaniko/executor version

echo "[TEST] Checking the '/kaniko/update-docker-config.sh' script exists" && \
    if [ ! -f /kaniko/update-docker-config.sh ];
    then
        echo "[ERROR] The file '/kaniko/update-docker-config.sh' does not exist"
        exit 1
    fi

echo "[TEST] Checking the '/kaniko/update-docker-config.sh' script is executable" && \
    if [ ! -x "/kaniko/update-docker-config.sh" ];
    then 
        echo "[ERROR] The file '/kaniko/update-docker-config.sh' does not executable"
        exit 1
    fi
