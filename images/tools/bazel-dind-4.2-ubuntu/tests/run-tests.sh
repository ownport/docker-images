#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out bazel version' && \
    bazel --version

echo '[TEST] Check dockerd version' && \
    dockerd --version

echo '[TEST] Check docker version' && \
    docker --version
