#!/bin/sh

set -e

echo "[INFO] Run tests"

echo "[TEST] Print out Kaniko version" && \
    /kaniko/executor version

echo "[TEST] Checking the '/kaniko/update-docker-config.sh' script exists" && \
    [ ! -f /kaniko/update-docker-config.sh ] && {
        echo "[ERROR] The file '/kaniko/update-docker-config.sh' does not exist"
        exit 1
    }

echo "[TEST] Checking the '/kaniko/update-docker-config.sh' script is executable" && \
    [ ! -x "/kaniko/update-docker-config.sh" ] && {
        echo "[ERROR] The file '/kaniko/update-docker-config.sh' does not executable"
        exit 1
    }
