#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out Kaniko version' && \
    executor version

echo '[TEST] Print out Python3 version' && \
    python3 --version

echo '[TEST] Print out Git version' && \
    git --version
